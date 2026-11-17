# Veridata Compliance Research Group website

A single static page (HTML and CSS, no build step, no JavaScript) published with GitHub Pages.

| File | Purpose |
|---|---|
| `index.html` | The page |
| `styles.css` | All styles (colors and spacing are variables at the top) |
| `favicon.svg` | Browser-tab icon (the logo's V mark) |
| `images/` | Logo files (`logo.png` for the header, `logo-white.png` for the dark footer, `apple-touch-icon.png` for phone home screens) and stock photos, two sizes each (see Photo credits below) |
| `README.md` | These instructions |

## Preview locally

Double-click `index.html` to open it in a browser, or serve the folder and open http://localhost:8000:

```bash
python -m http.server 8000
```

---

## 1. Create the repository

1. Sign in to GitHub with an account that is an **owner** of the `veridatacompliance` organization.
   No organization yet? Avatar menu → **Your organizations** → **New organization** → **Free**, and name it `veridatacompliance`.
2. Go to https://github.com/new.
3. **Owner:** `veridatacompliance`. **Repository name:** `veridatacompliance.github.io`, spelled exactly like that. That name is what makes it the organization's main site.
4. **Visibility:** Public. GitHub Pages is free for public repositories.
5. Leave "Add a README", ".gitignore", and "license" off, then click **Create repository**.

## 2. Push the files

**Option A: command line** (needs Git installed)

```bash
cd path/to/this/folder
git init -b main
git config user.name "VCRG"
git config user.email "info@veridatacompliance.org"
git add index.html styles.css favicon.svg README.md images
git commit -m "Initial site"
git remote add origin https://github.com/veridatacompliance/veridatacompliance.github.io.git
git push -u origin main
```

The two `git config` lines set the commit author for this repository only. In a public repository, commit author names and emails are visible to anyone.

**Option B: upload in the browser**

On the new, empty repository page, click **uploading an existing file**, drag in `index.html`, `styles.css`, `favicon.svg`, `README.md`, and the whole `images` folder, then click **Commit changes**. After it finishes, check that the repository shows an `images` folder with 18 files inside.

## 3. Turn on GitHub Pages

1. In the repository, open **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Set **Branch** to `main` and the folder to `/ (root)`, then click **Save**. (It may already be set this way. If so, there's nothing to change.)
4. After a minute or two the site is live at **https://veridatacompliance.github.io/**. You can watch progress in the **Actions** tab ("pages build and deployment"). When it finishes, the Pages settings screen shows a **Visit site** button.

To update the site later, edit the files and commit to `main`. GitHub redeploys automatically.

---

## 4. Optional: use veridatacompliance.org

Do steps 4a–4d in one sitting. Once the custom domain is saved (4c), `veridatacompliance.github.io` starts redirecting to `veridatacompliance.org`, so the DNS records (4b) should already be in place.

### 4a. Verify the domain (recommended)

Verifying stops anyone else from attaching the domain to their own GitHub Pages site.

1. Organization page → **Settings** → **Pages** (under "Code, planning, and automation") → **Add a domain**.
2. Enter `veridatacompliance.org`. GitHub shows a TXT record to create.
3. At your DNS provider, add that TXT record. The host/name looks like `_github-pages-challenge-veridatacompliance` and the value is the code GitHub shows.
4. Back on GitHub, click **Verify**. If it fails at first, wait a few minutes for DNS to update and try again.

### 4b. Add the DNS records

At the DNS provider for `veridatacompliance.org`:

| Type | Name / Host | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA (optional, IPv6) | `@` | `2606:50c0:8000::153` |
| AAAA (optional, IPv6) | `@` | `2606:50c0:8001::153` |
| AAAA (optional, IPv6) | `@` | `2606:50c0:8002::153` |
| AAAA (optional, IPv6) | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `veridatacompliance.github.io` |

- Delete any other A or AAAA records on `@` (for example, a registrar's "parked" page), turn off any domain or URL forwarding, and don't add a wildcard (`*`) record.
- If `www` already has a record, replace it with the CNAME above.
- **Leave email records alone.** Don't change MX records or email-related TXT/CNAME records (SPF, DKIM, DMARC, autodiscover, other verification TXT records). The website records above don't affect email.

### 4c. Add the custom domain (this creates the CNAME file)

1. Repository → **Settings → Pages → Custom domain**: enter `veridatacompliance.org` and click **Save**.
2. GitHub commits a file named `CNAME` to the repository root containing `veridatacompliance.org`. If you push from the command line, run `git pull` before your next push.

   To do it by hand instead, create a file named `CNAME` (all caps, no extension) in the repository root containing this single line, then commit it and confirm the domain appears under **Settings → Pages**:

   ```
   veridatacompliance.org
   ```

### 4d. Turn on HTTPS

1. Wait for the DNS check under **Settings → Pages** to pass. This usually takes minutes to a few hours; DNS changes can take up to 48 hours to spread.
2. Tick **Enforce HTTPS** when it becomes available. GitHub issues the certificate automatically, which can take up to an hour after DNS resolves.

With both `@` and `www` set up, GitHub redirects `www.veridatacompliance.org` to `veridatacompliance.org`.

To check DNS from a terminal (it should list the four `185.199.x.153` addresses):

```bash
nslookup veridatacompliance.org
```

**Note:** once the organization site uses this domain, any other GitHub Pages sites published from repositories in the `veridatacompliance` organization that don't have their own custom domain are served under it, at `veridatacompliance.org/<repository-name>`.

---

## 5. Optional: help Google find it

A new site can take days to weeks to appear in search results. To speed that up, add the site in [Google Search Console](https://search.google.com/search-console), verify it (a DNS TXT record for the custom domain, or the HTML-tag method for the `github.io` address), then use **URL Inspection → Request indexing** on the home page.

## Editing notes

- To change the contact address, search `index.html` for `info@veridatacompliance.org`. It appears in several places (top bar, Contact section, footer).
- The questions section and the footer both say the site doesn't use cookies or analytics. If analytics are ever added, update both.
- To update the logo, replace `images/logo.png` (navy and teal, for light backgrounds) and `images/logo-white.png` (white and teal, for the navy footer) with files of the same proportions.
- Each photo comes in two widths (for example `desk-640.jpg` and `desk-1200.jpg`). To swap one, replace both files with the same names and similar proportions, or update the `src`/`srcset` lines in `index.html`.

## Photo credits

All photos are from [Unsplash](https://unsplash.com) and used under the [Unsplash License](https://unsplash.com/license), which allows free commercial use without attribution. Credits are listed here for reference.

| File | Photo | Photographer |
|---|---|---|
| `hero-*.jpg` | [Low angle photo of city high rise buildings](https://unsplash.com/photos/low-angle-photo-of-city-high-rise-buildings-during-daytime-PhYq704ffdA) | Sean Pollock |
| `about-*.jpg` | [Hallway between glass-panel doors](https://unsplash.com/photos/hallway-between-glass-panel-doors-yWwob8kwOCk) | Nastuh Abootalebi |
| `desk-*.jpg` | [A wooden table topped with papers and a pen](https://unsplash.com/photos/a-wooden-table-topped-with-papers-and-a-pen-spScdgWY-_c) | 2H Media |
| `folders-*.jpg` | [A stack of thick folders on a white surface](https://unsplash.com/photos/a-stack-of-thick-folders-on-a-white-surface-XN4T2PVUUgk) | Beatriz Pérez Moya |
| `laptop-*.jpg` | [Laptop computer on glass-top table](https://unsplash.com/photos/laptop-computer-on-glass-top-table-hpjSkU2UYSU) | Carlos Muza |
| `meeting-*.jpg` | [A glass walled meeting room with a table and chairs](https://unsplash.com/photos/a-glass-walled-meeting-room-with-a-table-and-chairs-fxIcYymZHJg) | Hammer Group |
| `band-*.jpg` | [Low angle photo of curtain wall building](https://unsplash.com/photos/low-angle-photo-of-curtain-wall-building-1FxMET2U5dU) | Héctor J. Rivas |
