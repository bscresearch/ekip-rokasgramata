# EKIP — Rokasgrāmata

**Sadarbība viedai un ilgtspējīgai teritoriālai attīstībai**

Latvian handbook published in 2022 by Baltic Studies Centre. Illustrations by Daina Jurķe. Full author credits appear on the homepage.

This folder contains the current cleaned website without any previous Git history or remote configuration.

## Structure

- `site/` — editable HTML pages, feeds, sitemap and manifest.
- `site/assets/` — images, icons, styles, scripts, fonts and bundled rendering libraries.
- `scripts/build.py` — generates the website for a specified public URL.
- `scripts/check.py` — checks local links and asset references in the generated website.
- `dist/` — build output, generated when needed and excluded from Git.

The site was recovered from generated Hugo HTML. Original Hugo Markdown and templates were not available. Edit pages under `site/`; shared navigation is repeated across pages. Update `site/assets/js/search-data.json` when changing searchable page text. Preserve `__SITE_BASE__` tokens: the build replaces them with the chosen publishing URL.

## Local preview

Requires Python 3; no additional packages are needed.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/. Stop any previous server using port 8000 first. Search requires an HTTP server rather than opening HTML files directly.

## Start a new GitHub repository

Create an empty repository named `ekip-rokasgramata` on your GitHub account. From this folder, initialize a fresh history:

```sh
git init -b main
git add .
git commit -m "Initial handbook website"
git remote add origin https://github.com/krista-qp/ekip-rokasgramata.git
git push -u origin main
```

This folder uses a new Git history starting with the cleaned website; none of the former repository history is included. Publishing the website is a separate step from pushing the repository.

## Build for publishing

```sh
python3 scripts/build.py --base-url https://krista-qp.github.io/ekip-rokasgramata/
python3 scripts/check.py
```

Publish the **contents of `dist/`**, not `site/` or the repository root. GitHub Pages requires a deployment workflow that builds and uploads this directory, or a separate branch containing the generated files. No automatic deployment is configured here.

## Images and content

All three topic illustrations are stored locally. The homepage uses the digitalisation illustration in place of the unavailable original cover. The direct-sales chapter includes two market/farm photographs with matching display crops. No placeholder images remain in this folder.

The substantive handbook text is historical material published in 2022; website cleanup does not constitute a full content update. The separate editorial review and recovery records remain in the original local `ekip` folder.

Author and theme credits are retained. No new license is assigned by this cleanup.
