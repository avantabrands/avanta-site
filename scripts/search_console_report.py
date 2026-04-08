#!/usr/bin/env python3
"""Generate a lightweight Google Search Console performance report.

Supports either:
- OAuth desktop app credentials stored locally, or
- a service account JSON key that has been added to the Search Console property.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
API_BASE = "https://www.googleapis.com/webmasters/v3"
DEFAULT_OUTPUT_DIR = Path("reports/search-console")
DEFAULT_TOKEN_FILE = Path("secrets/gsc-token.json")
DEFAULT_CLIENT_SECRETS = Path("secrets/gsc-oauth-client.json")
DEFAULT_SERVICE_ACCOUNT = Path("secrets/gsc-service-account.json")


@dataclass
class ReportWindow:
    start: str
    end: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--property",
        required=True,
        help="Search Console property, e.g. sc-domain:avantabrands.co or https://avantabrands.co/",
    )
    parser.add_argument("--days", type=int, default=28, help="Trailing days to analyze.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for markdown/json output.",
    )
    parser.add_argument(
        "--auth-mode",
        choices=["oauth", "service-account", "auto"],
        default="auto",
        help="Authentication mode. Auto prefers service-account if configured.",
    )
    return parser.parse_args()


def get_window(days: int, offset_days: int = 0) -> ReportWindow:
    end = date.today() - timedelta(days=3 + offset_days)
    start = end - timedelta(days=days - 1)
    return ReportWindow(start.isoformat(), end.isoformat())


def load_credentials(auth_mode: str) -> Credentials:
    service_account_file = Path(
        os.environ.get("GSC_SERVICE_ACCOUNT_FILE", DEFAULT_SERVICE_ACCOUNT)
    )
    client_secrets_file = Path(
        os.environ.get("GSC_CLIENT_SECRETS_FILE", DEFAULT_CLIENT_SECRETS)
    )
    token_file = Path(os.environ.get("GSC_TOKEN_FILE", DEFAULT_TOKEN_FILE))

    if auth_mode in {"service-account", "auto"} and service_account_file.exists():
        return service_account.Credentials.from_service_account_file(
            str(service_account_file), scopes=SCOPES
        )

    if auth_mode == "service-account":
        raise SystemExit(
            f"Service account credentials not found at {service_account_file}."
        )

    creds: Credentials | None = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        if not client_secrets_file.exists():
            raise SystemExit(
                "OAuth client secrets not found. Add them to "
                f"{client_secrets_file} or set GSC_CLIENT_SECRETS_FILE."
            )
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secrets_file), SCOPES
        )
        creds = flow.run_local_server(port=0)
        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    return creds


def post_json(
    creds: Credentials, property_name: str, path: str, payload: dict[str, Any]
) -> dict[str, Any]:
    if not creds.valid:
        creds.refresh(Request())
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }
    property_path = quote(property_name, safe="")
    response = requests.post(
        f"{API_BASE}/sites/{property_path}/{path}",
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def fetch_rows(
    creds: Credentials,
    property_name: str,
    window: ReportWindow,
    dimensions: list[str],
    row_limit: int = 25,
) -> list[dict[str, Any]]:
    payload = {
        "startDate": window.start,
        "endDate": window.end,
        "dimensions": dimensions,
        "rowLimit": row_limit,
    }
    data = post_json(creds, property_name, "searchAnalytics/query", payload)
    return data.get("rows", [])


def row_dict(row: dict[str, Any], dimensions: list[str]) -> dict[str, Any]:
    values = dict(zip(dimensions, row.get("keys", []), strict=False))
    values.update(
        {
            "clicks": round(row.get("clicks", 0), 2),
            "impressions": round(row.get("impressions", 0), 2),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 2),
        }
    )
    return values


def summarize(rows: list[dict[str, Any]], dimensions: list[str]) -> list[dict[str, Any]]:
    return [row_dict(row, dimensions) for row in rows]


def top_opportunities(
    page_query_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = [row_dict(row, ["page", "query"]) for row in page_query_rows]
    filtered = [
        row
        for row in rows
        if row["impressions"] >= 30 and row["position"] <= 20 and row["ctr"] < 3.5
    ]
    return sorted(filtered, key=lambda item: (-item["impressions"], item["position"]))[:10]


def totals(rows: list[dict[str, Any]]) -> dict[str, float]:
    return {
        "clicks": round(sum(row.get("clicks", 0) for row in rows), 2),
        "impressions": round(sum(row.get("impressions", 0) for row in rows), 2),
    }


def format_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No data returned yet._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def build_markdown(
    property_name: str,
    current_window: ReportWindow,
    previous_window: ReportWindow,
    pages: list[dict[str, Any]],
    queries: list[dict[str, Any]],
    opportunities: list[dict[str, Any]],
) -> str:
    page_totals = totals(pages)
    query_totals = totals(queries)
    lines = [
        f"# Search Console Report: {property_name}",
        "",
        f"- Current window: `{current_window.start}` to `{current_window.end}`",
        f"- Previous comparison window: `{previous_window.start}` to `{previous_window.end}`",
        "",
        "## Snapshot",
        "",
        f"- Top-page clicks in current window: **{page_totals['clicks']}**",
        f"- Top-page impressions in current window: **{page_totals['impressions']}**",
        f"- Top-query clicks in current window: **{query_totals['clicks']}**",
        f"- Top-query impressions in current window: **{query_totals['impressions']}**",
        "",
        "## Top Pages",
        "",
        format_table(pages, ["page", "clicks", "impressions", "ctr", "position"]),
        "",
        "## Top Queries",
        "",
        format_table(queries, ["query", "clicks", "impressions", "ctr", "position"]),
        "",
        "## Best CTR Opportunities",
        "",
        "These are page/query combinations with impressions already building, positions in a workable range, and CTR still low enough to improve with stronger titles, proof, and internal links.",
        "",
        format_table(
            opportunities,
            ["page", "query", "clicks", "impressions", "ctr", "position"],
        ),
        "",
    ]
    return "\n".join(lines)


def write_outputs(output_dir: Path, report: dict[str, Any], markdown: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "latest.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    (output_dir / "latest.md").write_text(markdown, encoding="utf-8")


def main() -> None:
    args = parse_args()
    creds = load_credentials(args.auth_mode)

    current_window = get_window(args.days)
    previous_window = get_window(args.days, offset_days=args.days)

    current_pages_raw = fetch_rows(
        creds, args.property, current_window, ["page"], row_limit=20
    )
    current_queries_raw = fetch_rows(
        creds, args.property, current_window, ["query"], row_limit=20
    )
    current_page_query_raw = fetch_rows(
        creds, args.property, current_window, ["page", "query"], row_limit=50
    )

    report = {
        "property": args.property,
        "current_window": current_window.__dict__,
        "previous_window": previous_window.__dict__,
        "top_pages": summarize(current_pages_raw, ["page"]),
        "top_queries": summarize(current_queries_raw, ["query"]),
        "opportunities": top_opportunities(current_page_query_raw),
    }

    markdown = build_markdown(
        args.property,
        current_window,
        previous_window,
        report["top_pages"],
        report["top_queries"],
        report["opportunities"],
    )
    write_outputs(Path(args.output_dir), report, markdown)
    print(f"Wrote Search Console report to {Path(args.output_dir) / 'latest.md'}")


if __name__ == "__main__":
    main()
