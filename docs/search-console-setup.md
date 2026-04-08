# Search Console Access And Monitoring

This setup keeps us on the safe side:

- use the sitemap for bulk discovery
- use manual `Request indexing` only for important new or materially updated pages
- use API access for reporting and monitoring only

## What To Avoid

- Do not request indexing for every page every day.
- Do not resubmit unchanged URLs repeatedly.
- Do not use any unofficial indexing hacks.

## Search Console Access

The Google account already logged into this Mac should have access to the `avantabrands.co` property.

To confirm inside Search Console:

1. Open [Google Search Console](https://search.google.com/search-console)
2. Select the `avantabrands.co` property
3. Go to `Settings`
4. Open `Users and permissions`
5. Confirm `avantabrands@gmail.com` has `Owner` or `Full` access

Google help:

- [Manage owners, users, and permissions](https://support.google.com/webmasters/answer/7687615?hl=en)
- [Add a Search Console property](https://support.google.com/webmasters/answer/34592?hl=en)

## One-Time API Setup

This is the cleanest way to let local scripts monitor Search Console safely.

1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project like `Avanta Search Console`
3. Enable the `Google Search Console API`
4. Open `APIs & Services` -> `Credentials`
5. Create an `OAuth client ID`
6. Choose `Desktop app`
7. Download the JSON file
8. Save it locally to:

```text
secrets/gsc-oauth-client.json
```

If you prefer service accounts instead:

1. Create a service account in Google Cloud
2. Download the JSON key
3. Save it locally to:

```text
secrets/gsc-service-account.json
```

4. Add the service account email to the Search Console property as a user

## Run The Report

From the repo root:

```bash
python3 scripts/search_console_report.py --property sc-domain:avantabrands.co
```

If the property is a URL-prefix property instead of a domain property, use:

```bash
python3 scripts/search_console_report.py --property https://avantabrands.co/
```

The first OAuth run opens a browser window so Google can approve read-only access. After that, the refresh token is stored locally and the script can run unattended.

Outputs:

- `reports/search-console/latest.md`
- `reports/search-console/latest.json`

## Priority Pages To Submit Manually

Use `Request indexing` in URL Inspection for these first:

- `https://avantabrands.co/`
- `https://avantabrands.co/services/`
- `https://avantabrands.co/services/tiktok-shop-agency/`
- `https://avantabrands.co/services/tiktok-shop-management/`
- `https://avantabrands.co/services/tiktok-shop-agency-for-beauty-brands/`
- `https://avantabrands.co/case-studies/`
- `https://avantabrands.co/case-studies/beauty-brand-tiktok-shop-scale/`
- `https://avantabrands.co/guides/`
- `https://avantabrands.co/guides/what-does-a-tiktok-shop-agency-do/`
- `https://avantabrands.co/guides/how-to-choose-a-tiktok-shop-agency/`

## Safe Operating Rhythm

- Submit `sitemap.xml` once, then again only when the URL set materially changes
- Request indexing only for new or heavily updated URLs
- Review Search Console weekly for:
  - indexing coverage
  - rising queries
  - low-CTR pages with impressions
  - branded query growth
