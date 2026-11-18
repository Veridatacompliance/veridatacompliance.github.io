# Veridata Compliance Research Group website

A static, multi-page website (HTML and CSS, plus one small script for the mobile menu) published with GitHub Pages at **https://veridatacompliance.org**.

## What's in this repository

| Path | Purpose |
|---|---|
| `index.html` | Home page |
| `about/`, `services/`, `approach/`, `insights/`, `careers/`, `contact/`, `privacy/`, `terms/` | Inner pages (each folder holds an `index.html`) |
| `services/<service>/`, `insights/<essay>/` | Individual service pages and essays |
| `404.html` | Page shown for addresses that don't exist |
| `styles.css` | All styles (colors and spacing are variables at the top) |
| `site.js` | The mobile menu (no tracking, no cookies) |
| `favicon.svg` | Browser-tab icon (the logo's V mark) |
| `images/` | Logo files (`logo.png`, `logo-white.png`, `apple-touch-icon.png`, `og-image.png` for link previews) and stock photos |
| `sitemap.xml`, `robots.txt` | Help search engines find every page |
| `CNAME` | Tells GitHub Pages to serve the site at veridatacompliance.org |
| `_build/` | The page builder and the wording for every page (not published, because the folder name starts with an underscore) |

## Preview locally

The pages use site-root links (for example `/styles.css`), so open them through a small local web server rather than by double-clicking. From this folder:

```bash
python -m http.server 8000
```

then open http://localhost:8000.

## Changing the wording

All page wording lives in two files:

- `_build/content/home.json`: the home page, plus the shared top bar and footer text.
- `_build/content/pages.json`: every other page.

After editing either file, rebuild the pages:

```bash
python _build/build.py
```

On the computer that maintains the site, a local checker (`_build/check.py`, kept out of this repository) looks for broken links, missing images, duplicate titles, and wording the site avoids. Run it after each build:

```bash
python _build/check.py
```

Shared parts of the layout (header, menu, footer, page sections) are in `_build/build.py`. Editing the generated HTML by hand also works, but the next build overwrites those edits.

## Publishing changes

GitHub Pages publishes whatever is on the `main` branch:

```bash
git add -A
```

```bash
git commit -m "Describe the change"
```

```bash
git push
```

The site updates within a minute or two. Pushes from this folder sign in as the `Veridatacompliance` GitHub account; the commit author is set to "VCRG" for this repository only. After changing `styles.css` or `site.js`, also change `ASSET_VERSION` in `_build/build.py` and rebuild, so browsers fetch the new files right away.

## Domain and DNS (already set up)

The domain is managed at GoDaddy. GitHub Pages needs these records, which are in place:

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | veridatacompliance.github.io |

The email records (MX, SPF and DKIM TXT/CNAME records, autodiscover) belong to Microsoft 365. Leave them unchanged.

In the repository's **Settings → Pages**, the custom domain is `veridatacompliance.org` and **Enforce HTTPS** is on.

## Photo credits

All photos are from [Unsplash](https://unsplash.com) and used under the [Unsplash License](https://unsplash.com/license), which allows free commercial use without attribution. Credits are listed here for reference.

| Files | Photo | Photographer |
|---|---|---|
| `hero-*.jpg` | [Low angle photo of city high rise buildings](https://unsplash.com/photos/low-angle-photo-of-city-high-rise-buildings-during-daytime-PhYq704ffdA) | Sean Pollock |
| `about-*.jpg` | [Hallway between glass-panel doors](https://unsplash.com/photos/hallway-between-glass-panel-doors-yWwob8kwOCk) | Nastuh Abootalebi |
| `desk-*.jpg`, `desk-hero-*.jpg` | [A wooden table topped with papers and a pen](https://unsplash.com/photos/a-wooden-table-topped-with-papers-and-a-pen-spScdgWY-_c) | 2H Media |
| `folders-*.jpg`, `folders-hero-*.jpg` | [A stack of thick folders on a white surface](https://unsplash.com/photos/a-stack-of-thick-folders-on-a-white-surface-XN4T2PVUUgk) | Beatriz Pérez Moya |
| `laptop-*.jpg`, `laptop-hero-*.jpg` | [Laptop computer on glass-top table](https://unsplash.com/photos/laptop-computer-on-glass-top-table-hpjSkU2UYSU) | Carlos Muza |
| `meeting-*.jpg`, `meeting-hero-*.jpg` | [A glass walled meeting room with a table and chairs](https://unsplash.com/photos/a-glass-walled-meeting-room-with-a-table-and-chairs-fxIcYymZHJg) | Hammer Group |
| `band-*.jpg` | [Low angle photo of curtain wall building](https://unsplash.com/photos/low-angle-photo-of-curtain-wall-building-1FxMET2U5dU) | Héctor J. Rivas |
| `glass-*.jpg` | [Architectural photography of glass building](https://unsplash.com/photos/architectural-photography-of-glass-building-T0iFfJw-rB0) | Christian Ladewig |
| `towers-*.jpg` | [Low angle photography of high rise building](https://unsplash.com/photos/low-angle-photography-of-high-rise-building-ISQ3M9fPa0g) | Rafael Garcin |
| `stepped-*.jpg` | [Modern glass skyscraper with stepped facade](https://unsplash.com/photos/modern-glass-skyscraper-with-stepped-facade-0d-z8cJGIR4) | Parrish Freeman |
| `curve-*.jpg` | [Low-angle photography of blue glass walled building](https://unsplash.com/photos/low-angle-photography-of-blue-glass-walled-building-during-daytime-WXwQ-wj-g9Q) | Vojtech Bruzek |
| `writing-*.jpg` | [Man writing on paper](https://unsplash.com/photos/man-writing-on-paper-OQMZwNd3ThU) | Scott Graham |
| `workspace-*.jpg` | [Photo of dining table and chairs inside room](https://unsplash.com/photos/photo-of-dining-table-and-chairs-inside-room-eHD8Y1Znfpk) | Nastuh Abootalebi |
