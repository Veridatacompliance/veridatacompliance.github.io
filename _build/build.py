#!/usr/bin/env python3
"""Build the Veridata Compliance Research Group website from its content files.

Run from anywhere:  python _build/build.py

Reads _build/content/home.json and _build/content/pages.json and writes every page
(index.html, about/index.html, services/..., insights/..., and so on), plus 404.html,
sitemap.xml and robots.txt, into the repository root that GitHub Pages serves.

Folders whose names start with an underscore (like this one) are not published.
Editing the generated HTML by hand also works, but running this script again
overwrites those edits, so change the content files instead.
"""
import json
import re
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTENT = HERE / "content"

SITE_URL = "https://veridatacompliance.org"
COMPANY = "Veridata Compliance Research Group"
EMAIL = "info@veridatacompliance.org"
UPDATED_HUMAN = "November 18, 2026"
UPDATED_ISO = "2026-11-18"
YEAR = "2026"
ASSET_VERSION = "20261118"  # bump to make browsers fetch fresh CSS/JS after changes

DISCLAIMER = "VCRG is a private research firm and is not affiliated with any government agency."

# Service pages: slug in the URL, the matching id used on the home page, display names, photo.
SERVICES = [
    {"slug": "research-and-analysis", "home_id": "research-and-analysis", "name": "Research and Analysis",
     "short": "Research and analysis", "photo": "laptop", "icon": "doc-search"},
    {"slug": "data-verification", "home_id": "data-verification", "name": "Data Verification and Quality Review",
     "short": "Data verification", "photo": "folders", "icon": "checklist"},
    {"slug": "organization-and-reporting", "home_id": "information-organization",
     "name": "Information Organization and Reporting", "short": "Organizing and reporting", "photo": "desk",
     "icon": "layers"},
    {"slug": "research-support", "home_id": "research-support", "name": "Ongoing Research Support",
     "short": "Research support", "photo": "meeting", "icon": "briefcase"},
]
ARTICLES = ["framing-the-question", "why-verification-matters", "from-information-to-insight"]
NAV = [("About", "/about/"), ("Services", "/services/"), ("Approach", "/approach/"),
       ("Insights", "/insights/"), ("Careers", "/careers/")]


# --------------------------------------------------------------------------- helpers

def t(s):
    """Escape a text node."""
    return escape(s, quote=False)


def a(s):
    """Escape an attribute value."""
    return escape(s, quote=True)


LINK_RE = re.compile(r"\[([^\]]+)\]\((/[a-z0-9/-]*)\)")


def plain(s):
    """Text with [label](/path/) links reduced to their labels (for meta tags and cards)."""
    return LINK_RE.sub(r"\1", s)


def rich(s):
    """Escape text, turn [label](/path/) into a site link and the contact address into a mailto link."""
    out = t(s).replace(EMAIL, f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    return LINK_RE.sub(r'<a href="\2">\1</a>', out)


ICONS = {
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.4-4.4"/>',
    "doc-search": '<path d="M11 21H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7l5 5v3"/><path d="M14 3v4a1 1 0 0 0 1 1h4"/>'
                  '<path d="M8.5 9.5H12M8.5 13H11"/><circle cx="16" cy="16" r="3.25"/><path d="m18.4 18.4 2.6 2.6"/>',
    "check": '<circle cx="12" cy="12" r="8.5"/><path d="m8.5 12.2 2.4 2.4 4.8-5"/>',
    "checklist": '<path d="m4 6 1.5 1.5 3-3M11.5 6H20"/><path d="m4 12 1.5 1.5 3-3M11.5 12H20"/>'
                 '<path d="m4 18 1.5 1.5 3-3M11.5 18H20"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/>'
                 '<path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7"/><path d="M3 12.5h18"/>',
    "chart": '<path d="M4 20h16"/><path d="M7 16v-5"/><path d="M12 16V7"/><path d="M17 16v-8"/>',
    "chat": '<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.5 3.5V17'
            'A2.5 2.5 0 0 1 4 14.5z"/>',
    "layers": '<path d="m12 3.5 8.5 4.5-8.5 4.5L3.5 8z"/><path d="m3.5 12 8.5 4.5 8.5-4.5"/>'
              '<path d="m3.5 16 8.5 4.5 8.5-4.5"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "compass": '<circle cx="12" cy="12" r="8.5"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    "lightbulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3.5a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2V17h5v-.6'
                 'c0-.8.4-1.5 1-2A6 6 0 0 0 12 3.5z"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4.5h11l-2 4 2 4H5"/>',
    "refresh": '<path d="M19.5 8.5A8 8 0 0 0 5 7.5"/><path d="M5 3.5v4h4"/><path d="M4.5 15.5A8 8 0 0 0 19 16.5"/>'
               '<path d="M19 20.5v-4h-4"/>',
    "sliders": '<path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "eye-off": '<path d="M3 3l18 18"/><path d="M10.6 6.1A9.5 9.5 0 0 1 12 6c5 0 8.5 4.5 9.5 6a17 17 0 0 1-2.6 3.2"/>'
               '<path d="M6.6 6.6A17 17 0 0 0 2.5 12c1 1.5 4.5 6 9.5 6a9 9 0 0 0 4.4-1.1"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/>',
    "users": '<circle cx="9" cy="8.5" r="3.5"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 5.2a3.5 3.5 0 0 1 0 6.6"/>'
             '<path d="M18 14.3A6 6 0 0 1 21 20"/>',
    "pen": '<path d="M4 20h4L19 9a2.8 2.8 0 0 0-4-4L4 16z"/><path d="m13.5 6.5 4 4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
}

RULES = [
    (("confiden", "discre", "privacy", "trust"), "lock"),
    (("verif", "accura", "quality", "review", "check", "valid"), "checklist"),
    (("research", "analys", "inquir", "insight", "examin", "curios"), "search"),
    (("organi", "structur", "manage", "format", "consolid", "compil"), "layers"),
    (("report", "summar", "present", "transparen"), "chart"),
    (("clar", "understand", "plain"), "lightbulb"),
    (("communicat", "respons", "dialog", "convers", "listen"), "chat"),
    (("support", "collabor", "relationship", "service", "assist", "team"), "briefcase"),
    (("focus", "precis", "purpose", "object", "detail", "care"), "target"),
    (("independen", "integrit", "principle", "impartial", "judg", "ethic"), "compass"),
    (("consisten", "method", "rigor", "disciplin", "process", "standard"), "check"),
    (("project", "defined", "single", "one-time"), "flag"),
    (("ongoing", "recurring", "continu", "retain"), "refresh"),
    (("custom", "tailor", "flexib", "scope", "bespoke", "adapt"), "sliders"),
    (("time", "pace", "prompt"), "clock"),
    (("writ", "draft"), "pen"),
]
FALLBACKS = ["search", "check", "layers", "chat", "target", "compass", "briefcase", "lightbulb"]


def pick_icon(title, used):
    low = title.lower()
    for keys, name in RULES:
        if name not in used and any(k in low for k in keys):
            used.add(name)
            return name
    for name in FALLBACKS:
        if name not in used:
            used.add(name)
            return name
    return "check"


def svg(name, size=24):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'focusable="false">{ICONS[name]}</svg>')


ARROW = '<span aria-hidden="true">&rarr;</span>'


def icon_tile(name):
    return f'<span class="icon-tile">{svg(name)}</span>'


def paras(items, first_lead=False, indent="          "):
    out = []
    for i, p in enumerate(items):
        cls = ' class="lead"' if (first_lead and i == 0) else ""
        out.append(f"{indent}<p{cls}>{rich(p)}</p>")
    return "\n".join(out)


def checklist(items, two_col=False, indent="          "):
    cls = "checklist checklist-2col" if two_col else "checklist"
    lis = "\n".join(f"{indent}  <li>{rich(x)}</li>" for x in items)
    return f'{indent}<ul class="{cls}" role="list">\n{lis}\n{indent}</ul>'


# --------------------------------------------------------------------------- page chrome

ORG_JSON_LD = (
    '\n  <script type="application/ld+json">'
    '{"@context":"https://schema.org","@type":"Organization",'
    f'"name":"{COMPANY}","alternateName":"VCRG","url":"{SITE_URL}/",'
    f'"logo":"{SITE_URL}/images/logo.png","email":"{EMAIL}"}}'
    '</script>'
)


def head(title, description, path):
    title, description = plain(title), plain(description)
    canonical = ""
    if path:
        url = SITE_URL + path
        canonical = f'\n  <link rel="canonical" href="{url}">\n  <meta property="og:url" content="{url}">'
    robots = "index, follow" if path else "noindex, follow"
    og_type = "article" if path and path.startswith("/insights/") and path != "/insights/" else "website"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t(title)}</title>
  <meta name="description" content="{a(description)}">
  <meta name="robots" content="{robots}">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#0c2238">{canonical}
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{COMPANY}">
  <meta property="og:title" content="{a(title)}">
  <meta property="og:description" content="{a(description)}">
  <meta property="og:image" content="{SITE_URL}/images/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{COMPANY} logo">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image:alt" content="{COMPANY} logo">

  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&amp;display=swap">
  <link rel="stylesheet" href="/styles.css?v={ASSET_VERSION}">
  <script>document.documentElement.className += " js"; window.addEventListener("load", function () {{ if (!window.vcrgMenu) document.documentElement.classList.remove("js"); }});</script>
  <script src="/site.js?v={ASSET_VERSION}" defer></script>{ORG_JSON_LD if path == "/" else ""}
</head>"""


def topbar(text):
    return f"""  <div class="topbar">
    <div class="container topbar-inner">
      <p>{t(text)}</p>
      <a href="mailto:{EMAIL}">
        {svg("mail", 16)}
        {EMAIL}
      </a>
    </div>
  </div>"""


def header(active):
    items = []
    for label, href in NAV:
        cur = ""
        if active == href:
            cur = ' aria-current="page"'
        elif active.startswith(href) and href != "/":
            cur = ' aria-current="true"'
        items.append(f'          <li><a href="{href}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if active == "/contact/" else ""
    items.append(f'          <li><a class="nav-cta" href="/contact/"{cur}>Contact</a></li>')
    nav_items = "\n".join(items)
    return f"""  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="/">
        <img class="brand-logo" src="/images/logo.png" width="800" height="146" alt="{COMPANY}">
      </a>

      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
        <svg class="icon-open" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        <svg class="icon-close" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6 6 18"/></svg>
        Menu
      </button>

      <nav class="site-nav" id="site-nav" aria-label="Primary">
        <ul>
{nav_items}
        </ul>
      </nav>
    </div>
  </header>"""


def footer(about_text):
    company_links = [("About", "/about/"), ("Approach", "/approach/"), ("Insights", "/insights/"),
                     ("Careers", "/careers/"), ("Contact", "/contact/")]
    company = "\n".join(f'              <li><a href="{h}">{t(l)}</a></li>' for l, h in company_links)
    services = "\n".join(f'              <li><a href="/services/{s["slug"]}/">{t(s["short"])}</a></li>' for s in SERVICES)
    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <a class="brand-footer" href="/">
            <img class="footer-logo" src="/images/logo-white.png" width="800" height="146" alt="{COMPANY}" loading="lazy" decoding="async">
          </a>
          <p class="footer-about">{t(about_text)}</p>
        </div>

        <nav class="footer-nav" aria-label="Footer">
          <div class="footer-col">
            <h2 class="footer-heading">Company</h2>
            <ul role="list">
{company}
            </ul>
          </div>
          <div class="footer-col">
            <h2 class="footer-heading">Services</h2>
            <ul role="list">
{services}
            </ul>
          </div>
          <div class="footer-col">
            <h2 class="footer-heading">Legal</h2>
            <ul role="list">
              <li><a href="/privacy/">Privacy</a></li>
              <li><a href="/terms/">Terms of Use</a></li>
            </ul>
          </div>
          <div class="footer-col footer-col-contact">
            <h2 class="footer-heading">Contact</h2>
            <ul role="list">
              <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            </ul>
          </div>
        </nav>
      </div>

      <section class="footer-privacy" aria-labelledby="footer-privacy-title">
        <h2 class="footer-heading" id="footer-privacy-title">Privacy</h2>
        <p>These informational pages do not use cookies or analytics, and we do not sell personal information collected through them. Read the full <a href="/privacy/">privacy notice</a>, or email <a href="mailto:{EMAIL}">{EMAIL}</a> with questions.</p>
      </section>

      <div class="footer-base">
        <p>&copy; {YEAR} {COMPANY}</p>
        <p>{DISCLAIMER}</p>
      </div>
    </div>
  </footer>"""


def document(path, title, description, active, main_html, site):
    return f"""{head(title, description, path)}
<body>
  <a class="skip-link" href="#main">Skip to content</a>

{topbar(site["topbar"])}

{header(active)}

  <main id="main">
{main_html}
  </main>

{footer(site["footerAbout"])}
</body>
</html>
"""


def breadcrumb(crumbs):
    if not crumbs:
        return ""
    items = []
    for label, href in crumbs:
        if href:
            items.append(f'<li><a href="{href}">{t(label)}</a></li>')
        else:
            items.append(f'<li aria-current="page">{t(label)}</li>')
    return f'        <nav class="breadcrumb" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>\n'


def page_hero(eyebrow, h1, lede, photo=None, crumbs=(), meta=None):
    cls = "page-hero" if photo else "page-hero page-hero-plain"
    media = ""
    if photo:
        media = f"""      <picture class="page-hero-media">
        <source media="(max-width: 40em)" srcset="/images/{photo}-800.jpg" width="800" height="600">
        <img src="/images/{photo}-1600.jpg" width="1600" height="900" alt="" fetchpriority="high" decoding="async">
      </picture>
"""
    meta_html = f'\n        <p class="page-hero-meta">{t(meta)}</p>' if meta else ""
    lede_html = f'\n        <p class="page-hero-lede">{rich(lede)}</p>' if lede else ""
    return f"""    <section class="{cls}" aria-labelledby="page-title">
{media}      <div class="container">
{breadcrumb(crumbs)}        <p class="eyebrow">{t(eyebrow)}</p>
        <h1 id="page-title">{t(h1)}</h1>{lede_html}{meta_html}
      </div>
    </section>"""


def section_head(eyebrow, h2, intro, hid):
    if intro:
        return f"""        <div class="section-head section-head-split">
          <div>
            <p class="eyebrow">{t(eyebrow)}</p>
            <h2 id="{hid}">{t(h2)}</h2>
          </div>
          <p class="section-intro">{rich(intro)}</p>
        </div>"""
    return f"""        <div class="section-head">
          <p class="eyebrow">{t(eyebrow)}</p>
          <h2 id="{hid}">{t(h2)}</h2>
        </div>"""


def wrap(inner, hid, tint=False, extra_cls=""):
    cls = "section" + (" section-tint" if tint else "") + (f" {extra_cls}" if extra_cls else "")
    return f"""    <section class="{cls}" aria-labelledby="{hid}">
      <div class="container">
{inner}
      </div>
    </section>"""


def text_split(eyebrow, h2, paragraphs, hid, tint=False, first_lead=True):
    inner = f"""        <div class="text-split">
          <div>
            <p class="eyebrow">{t(eyebrow)}</p>
            <h2 id="{hid}">{t(h2)}</h2>
          </div>
          <div class="text-split-body">
{paras(paragraphs, first_lead=first_lead, indent="            ")}
          </div>
        </div>"""
    return wrap(inner, hid, tint)


def split_photo(eyebrow, h2, paragraphs, photo_html, hid, extra="", tint=False, landscape=False):
    cls = "split split-landscape" if landscape else "split"
    inner = f"""        <div class="{cls}">
          <div class="split-copy">
            <p class="eyebrow">{t(eyebrow)}</p>
            <h2 id="{hid}">{t(h2)}</h2>
{paras(paragraphs, first_lead=True, indent="            ")}{extra}
          </div>
          <figure class="split-media">
            {photo_html}
          </figure>
        </div>"""
    return wrap(inner, hid, tint)


def img_portrait(name):
    return (f'<img src="/images/{name}-960.jpg" srcset="/images/{name}-640.jpg 640w, /images/{name}-960.jpg 960w" '
            f'sizes="(min-width: 72em) 420px, (min-width: 56em) 36vw, 100vw" width="960" height="1200" alt="" '
            f'loading="lazy" decoding="async">')


def img_landscape(name, sizes="(min-width: 72em) 540px, (min-width: 56em) 45vw, 100vw"):
    return (f'<img src="/images/{name}-1200.jpg" srcset="/images/{name}-640.jpg 640w, /images/{name}-1200.jpg 1200w" '
            f'sizes="{sizes}" width="1200" height="900" alt="" loading="lazy" decoding="async">')


def cards(items, cls="card card-accent", grid="card-grid card-grid-4", link=None, icons=True):
    used = set()
    out = []
    for it in items:
        icon = f"\n            {icon_tile(pick_icon(it['title'], used))}" if icons else ""
        more = ""
        if link:
            more = f'\n            <a class="text-link" href="{link[1]}">{t(link[0])} {ARROW}</a>'
        out.append(f"""          <li class="{cls}">{icon}
            <h3>{t(it["title"])}</h3>
            <p>{rich(it["text"])}</p>{more}
          </li>""")
    return f'        <ul class="{grid}" role="list">\n' + "\n".join(out) + "\n        </ul>"


def link_cards(entries, grid="card-grid card-grid-3"):
    """entries: dicts with title, text, href, more, and optional photo / kicker."""
    out = []
    for e in entries:
        media = ""
        if e.get("photo"):
            media = f"""
            <figure class="card-media">
              {img_landscape(e["photo"], "(min-width: 64em) 540px, (min-width: 40em) 50vw, 100vw")}
            </figure>"""
        kicker = f'\n            <p class="card-kicker">{t(e["kicker"])}</p>' if e.get("kicker") else ""
        icon = f"\n            {icon_tile(e['icon'])}" if e.get("icon") and not e.get("photo") else ""
        out.append(f"""          <li class="card link-card">{media}{icon}{kicker}
            <h3><a href="{e["href"]}">{t(e["title"])}</a></h3>
            <p>{rich(e["text"])}</p>
            <span class="more" aria-hidden="true">{t(e["more"])} &rarr;</span>
          </li>""")
    return f'        <ul class="{grid}" role="list">\n' + "\n".join(out) + "\n        </ul>"


def principles_list(items):
    out = []
    for i, it in enumerate(items, start=1):
        out.append(f"""          <li class="principle">
            <span class="principle-num" aria-hidden="true">{i:02d}</span>
            <h3>{t(it["title"])}</h3>
            <p>{rich(it["text"])}</p>
          </li>""")
    return '        <ol class="principles" role="list">\n' + "\n".join(out) + "\n        </ol>"


def steps_panel(title, steps, heading_tag="h3"):
    lis = []
    for i, s in enumerate(steps, start=1):
        lis.append(f"""            <li class="step">
              <span class="step-num" aria-hidden="true">{i:02d}</span>
              <{heading_tag}>{t(s["title"])}</{heading_tag}>
              <p>{rich(s["text"])}</p>
            </li>""")
    title_html = f'\n          <h3 class="process-title">{t(title)}</h3>' if title else ""
    step_tag = "h4" if title else "h3"
    body = "\n".join(lis).replace(f"<{heading_tag}>", f"<{step_tag}>").replace(f"</{heading_tag}>", f"</{step_tag}>")
    return f"""        <div class="process">{title_html}
          <ol class="steps" role="list">
{body}
          </ol>
        </div>"""


def faq_section(eyebrow, h2, intro, items, hid, tint=True):
    details = []
    for i, f in enumerate(items):
        details.append(f"""          <details class="faq"{" open" if i == 0 else ""}>
            <summary>{t(f["q"])}</summary>
            <p>{rich(f["a"])}</p>
          </details>""")
    intro_html = f'\n          <p class="section-intro">{rich(intro)}</p>' if intro else ""
    inner = f"""        <div class="faq-grid">
          <div class="faq-head">
            <p class="eyebrow">{t(eyebrow)}</p>
            <h2 id="{hid}">{t(h2)}</h2>{intro_html}
          </div>
          <div class="faq-list">
{chr(10).join(details)}
          </div>
        </div>"""
    cls = "section section-tint" if tint else "section"
    return f"""    <section class="{cls}" aria-labelledby="{hid}">
      <div class="container">
{inner}
      </div>
    </section>"""


def band(eyebrow, h2, note, hid="band-title"):
    return f"""    <section class="band" aria-labelledby="{hid}">
      <img class="band-media" src="/images/band-1920.jpg" srcset="/images/band-960.jpg 960w, /images/band-1920.jpg 1920w" sizes="100vw" width="1920" height="1080" alt="" loading="lazy" decoding="async">
      <div class="container">
        <p class="eyebrow">{t(eyebrow)}</p>
        <h2 id="{hid}">{t(h2)}</h2>
        <p class="band-note">{rich(note)}</p>
      </div>
    </section>"""


def cta_panel(h2, note, eyebrow="Contact", button=True, show_email=True, hid="cta-title", tight=False):
    side = []
    if show_email and EMAIL not in note:
        side.append(f"""            <p class="cta-email">
              <span class="cta-label">Email</span>
              <a href="mailto:{EMAIL}">{EMAIL}</a>
            </p>""")
    if button:
        side.append('            <a class="btn btn-primary" href="/contact/">Contact us</a>')
    side_html = ""
    if side:
        side_html = '\n          <div class="cta-side">\n' + "\n".join(side) + "\n          </div>"
    cls = "section section-tight-top" if tight else "section"
    return f"""    <section class="{cls}" aria-labelledby="{hid}">
      <div class="container">
        <div class="cta-panel">
          <div>
            <p class="eyebrow">{t(eyebrow)}</p>
            <h2 id="{hid}">{t(h2)}</h2>
            <p class="cta-note">{rich(note)}</p>
          </div>{side_html}
        </div>
      </div>
    </section>"""


# --------------------------------------------------------------------------- pages

def home_page(h, articles):
    hero = h["hero"]
    used = set()
    highlights = "\n".join(f"""          <li class="highlight">
            {icon_tile(pick_icon(x["title"], used))}
            <div>
              <h3>{t(x["title"])}</h3>
              <p>{rich(x["text"])}</p>
            </div>
          </li>""" for x in h["highlights"])

    about = h["about"]
    about_extra = "\n" + checklist(about["checklist"], two_col=True, indent="            ") + \
        f'\n            <a class="text-link" href="/about/">More about VCRG {ARROW}</a>'
    about_html = split_photo("About", about["h2"], [about["lead"]] + about["paragraphs"], img_portrait("about"),
                             "about-title", extra=about_extra)
    about_html = about_html.replace('<section class="section"', '<section class="section" id="about"', 1)

    by_home_id = {s["home_id"]: s for s in SERVICES}
    rows = []
    for n, item in enumerate(h["services"]["items"], start=1):
        svc = by_home_id[item["id"]]
        rows.append(f"""          <article class="media-row" id="{svc["home_id"]}" aria-labelledby="svc-{n}">
            <figure class="media-row-image">
              {img_landscape(svc["photo"])}
            </figure>
            <div class="media-row-body">
              {icon_tile(svc["icon"])}
              <h3 id="svc-{n}">{t(item["title"])}</h3>
              <p>{rich(item["text"])}</p>
{checklist(item["bullets"], indent="              ")}
              <a class="text-link" href="/services/{svc["slug"]}/">Learn more about {t(svc["short"].lower())} {ARROW}</a>
            </div>
          </article>""")
    services = h["services"]
    services_html = f"""    <section class="section section-tint" id="services" aria-labelledby="services-title">
      <div class="container">
{section_head("Services", services["h2"], services["intro"], "services-title")}
        <div class="media-rows">
{chr(10).join(rows)}
        </div>
      </div>
    </section>"""

    values = h["values"]
    values_html = wrap(section_head(values["eyebrow"], values["h2"], values["intro"], "values-title") + "\n" +
                       cards(values["items"]), "values-title")
    values_html = values_html.replace('<section class="section"', '<section class="section" id="values"', 1)

    ap = h["approach"]
    approach_inner = (section_head("Approach", "How we work", ap["intro"], "approach-title") + "\n" +
                      '        <h3 class="list-title">Our principles</h3>\n' +
                      principles_list(ap["principles"]) + "\n" + steps_panel(ap["processTitle"], ap["steps"]) +
                      f'\n        <a class="text-link" href="/approach/">See our approach in detail {ARROW}</a>')
    approach_html = wrap(approach_inner, "approach-title", tint=True).replace(
        '<section class="section section-tint"', '<section class="section section-tint" id="approach"', 1)

    eng = h["engagement"]
    engage_html = wrap(section_head(eng["eyebrow"], eng["h2"], eng["intro"], "engagement-title") + "\n" +
                       cards(eng["items"], cls="card card-soft", grid="card-grid card-grid-3",
                             link=("Get in touch", "/contact/")), "engagement-title")

    insights_html = wrap(section_head("Insights", "Perspectives on careful research",
                                      "Short reflections on framing questions, checking information, and "
                                      "presenting findings clearly.", "insights-title") + "\n" +
                         link_cards(articles), "insights-title", tint=True)

    main = f"""    <section class="hero" aria-labelledby="hero-title">
      <picture class="hero-media">
        <source media="(max-width: 40em)" srcset="/images/hero-720.jpg" width="720" height="960">
        <img src="/images/hero-1600.jpg" srcset="/images/hero-960.jpg 960w, /images/hero-1600.jpg 1600w" sizes="100vw" width="1600" height="1067" alt="" fetchpriority="high" decoding="async">
      </picture>
      <div class="container">
        <p class="eyebrow">{t(hero["eyebrow"])}</p>
        <h1 id="hero-title">{t(hero["h1"])}</h1>
        <p class="hero-lede">{rich(hero["lede"])}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="/contact/">{t(hero["ctaPrimary"])}</a>
          <a class="btn btn-secondary" href="/services/">{t(hero["ctaSecondary"])}</a>
        </div>
      </div>
    </section>

    <section class="highlights" aria-labelledby="highlights-title">
      <h2 class="visually-hidden" id="highlights-title">At a glance</h2>
      <div class="container">
        <ul class="highlight-list" role="list">
{highlights}
        </ul>
      </div>
    </section>

{about_html}

{services_html}

{band(h["band"]["eyebrow"], h["band"]["h2"], h["band"]["note"])}

{values_html}

{approach_html}

{engage_html}

{insights_html}

{cta_panel(h["contact"]["h2"], h["contact"]["note"])}"""
    return main


def about_page(p):
    intro = p["intro"]
    parts = [
        page_hero(p["hero"]["eyebrow"], p["hero"]["h1"], p["hero"]["lede"], "glass", [("Home", "/"), ("About", None)]),
        split_photo("Who we are", intro["h2"], intro["paragraphs"], img_portrait("about"), "intro-title"),
        band(p["purpose"]["eyebrow"], p["purpose"]["statement"], p["purpose"]["note"], "purpose-title"),
        wrap(section_head(p["values"]["eyebrow"], p["values"]["h2"], p["values"]["intro"], "values-title") + "\n" +
             cards(p["values"]["items"]), "values-title"),
        wrap(section_head(p["distinctives"]["eyebrow"], p["distinctives"]["h2"], p["distinctives"]["intro"],
                          "distinctives-title") + "\n" + principles_list(p["distinctives"]["items"]),
             "distinctives-title", tint=True),
        text_split("Independence", p["independence"]["h2"], p["independence"]["paragraphs"], "independence-title"),
    ]
    return "\n\n".join(parts)


def services_page(p, svc_pages):
    by_slug = {s["slug"]: s for s in SERVICES}
    entries = []
    for summ in p["summaries"]:
        svc = by_slug[summ["slug"]]
        entries.append({"title": svc["name"], "text": summ["text"], "href": f"/services/{svc['slug']}/",
                        "more": "Learn more", "photo": svc["photo"]})
    eng = p["engagement"]
    parts = [
        page_hero(p["hero"]["eyebrow"], p["hero"]["h1"], p["hero"]["lede"], "towers", [("Home", "/"), ("Services", None)]),
        text_split("Overview", p["intro"]["h2"], p["intro"]["paragraphs"], "intro-title"),
        wrap(section_head("Our services", "How we can help", None, "list-title") + "\n" +
             link_cards(entries, grid="card-grid"), "list-title", tint=True),
        wrap(section_head(eng["eyebrow"], eng["h2"], eng["intro"], "engagement-title") + "\n" +
             cards(eng["items"], cls="card card-soft", grid="card-grid card-grid-3",
                   link=("Get in touch", "/contact/")), "engagement-title"),
        cta_panel(p["closing"]["h2"], p["closing"]["text"], tight=True),
    ]
    return "\n\n".join(parts)


def service_page(svc, p, all_pages):
    others = [s for s in SERVICES if s["slug"] != svc["slug"]]
    related = []
    for o in others:
        op = all_pages.get("service-" + o["slug"], {})
        related.append({"title": o["name"], "text": (op.get("hero") or {}).get("lede", ""),
                        "href": f"/services/{o['slug']}/", "more": "Learn more", "icon": o["icon"]})
    inc = p["includes"]
    ap = p["approach"]
    parts = [
        page_hero("Services", svc["name"], p["hero"]["lede"], svc["photo"] + "-hero",
                  [("Home", "/"), ("Services", "/services/"), (svc["name"], None)]),
        split_photo("Overview", p["overview"]["h2"], p["overview"]["paragraphs"], img_landscape(svc["photo"]),
                    "overview-title", landscape=True),
        wrap(section_head("Scope", inc["h2"], inc["intro"], "includes-title") + "\n" +
             checklist(inc["bullets"], two_col=True, indent="        "), "includes-title", tint=True),
        wrap(section_head("How we work", ap["h2"], ap["intro"], "approach-title") + "\n" +
             principles_list(ap["items"]), "approach-title"),
        faq_section("Questions", f"Questions about {svc['short'].lower()}", None, p["faq"], "faq-title"),
        wrap(section_head("Related services", "Explore other services", None, "related-title") + "\n" +
             link_cards(related), "related-title"),
        cta_panel(p["closing"]["h2"], p["closing"]["text"], tight=True),
    ]
    return "\n\n".join(parts)


def approach_page(p):
    std = p["standards"]
    parts = [
        page_hero(p["hero"]["eyebrow"], p["hero"]["h1"], p["hero"]["lede"], "stepped", [("Home", "/"), ("Approach", None)]),
        text_split("Overview", p["intro"]["h2"], p["intro"]["paragraphs"], "intro-title"),
        wrap(section_head("Principles", "What guides our conduct", None, "principles-title") + "\n" +
             principles_list(p["principles"]), "principles-title", tint=True),
        wrap(section_head("Process", p["process"]["h2"], p["process"]["intro"], "process-title") + "\n" +
             steps_panel(None, p["process"]["steps"]), "process-title"),
        wrap(section_head("Standards", std["h2"], std["intro"], "standards-title") + "\n" +
             checklist(std["bullets"], two_col=True, indent="        "), "standards-title", tint=True),
        text_split("Collaboration", p["collaboration"]["h2"], p["collaboration"]["paragraphs"], "collab-title"),
        cta_panel(HOME_CONTACT["h2"], HOME_CONTACT["note"], tight=True),
    ]
    return "\n\n".join(parts)


def article_entries(pages):
    entries = []
    for slug in ARTICLES:
        ap = pages["article-" + slug]
        entries.append({"title": ap["hero"]["h1"], "text": ap["summary"], "href": f"/insights/{slug}/",
                        "more": "Read the essay", "kicker": "Perspective"})
    return entries


def insights_page(p, pages):
    parts = [
        page_hero(p["hero"]["eyebrow"], p["hero"]["h1"], p["hero"]["lede"], "writing", [("Home", "/"), ("Insights", None)]),
        wrap(section_head("Perspectives", p["intro"]["h2"], p["intro"]["paragraph"], "intro-title") + "\n" +
             link_cards(article_entries(pages)), "intro-title"),
        cta_panel(HOME_CONTACT["h2"], HOME_CONTACT["note"], tight=True),
    ]
    return "\n\n".join(parts)


def article_page(slug, p, pages):
    body = []
    for i, s in enumerate(p["sections"]):
        body.append(f"            <h2>{t(s['h2'])}</h2>")
        body.append(paras(s["paragraphs"], indent="            "))
    take = checklist(p["takeaways"], indent="              ")
    others = [x for x in ARTICLES if x != slug]
    links = "\n".join(
        f'              <li><a href="/insights/{o}/">{t(pages["article-" + o]["hero"]["h1"])}</a></li>' for o in others)
    article = f"""    <section class="section" aria-label="Essay">
      <div class="container">
        <div class="article-layout">
          <article class="prose">
{chr(10).join(body)}
            <aside class="takeaways" aria-labelledby="takeaways-title">
              <h2 id="takeaways-title">Key points</h2>
{take}
            </aside>
          </article>
          <aside class="article-aside" aria-labelledby="more-title">
            <h2 id="more-title">More perspectives</h2>
            <ul role="list">
{links}
              <li><a href="/insights/">All insights {ARROW}</a></li>
            </ul>
          </aside>
        </div>
      </div>
    </section>"""
    parts = [
        page_hero("Perspective", p["hero"]["h1"], p["hero"]["lede"], None,
                  [("Home", "/"), ("Insights", "/insights/"), (p["hero"]["h1"], None)]),
        article,
        cta_panel(HOME_CONTACT["h2"], HOME_CONTACT["note"], tight=True),
    ]
    return "\n\n".join(parts)


def careers_page(p):
    q = p["qualities"]
    interest = p["interest"]
    parts = [
        page_hero(p["hero"]["eyebrow"], p["hero"]["h1"], p["hero"]["lede"], "workspace", [("Home", "/"), ("Careers", None)]),
        text_split("Working at VCRG", p["intro"]["h2"], p["intro"]["paragraphs"], "intro-title"),
        wrap(section_head("What we value", q["h2"], q["intro"], "qualities-title") + "\n" + cards(q["items"]),
             "qualities-title", tint=True),
        cta_panel(interest["h2"], " ".join(interest["paragraphs"]), eyebrow="Future opportunities", button=False),
    ]
    return "\n\n".join(parts)


def contact_page(p, home):
    inc = p["include"]
    nxt = p["next"]
    panel = f"""    <section class="section" aria-labelledby="email-title">
      <div class="container">
        <div class="cta-panel">
          <div>
            <p class="eyebrow">Email</p>
            <h2 id="email-title">{t(home["contact"]["h2"])}</h2>
            <p class="cta-note">{rich(p["panelNote"])}</p>
          </div>
          <div class="cta-side">
            <p class="cta-email">
              <span class="cta-label">Email</span>
              <a href="mailto:{EMAIL}">{EMAIL}</a>
            </p>
          </div>
        </div>
      </div>
    </section>"""
    parts = [
        page_hero(p["hero"]["eyebrow"], p["hero"]["h1"], p["hero"]["lede"], "curve", [("Home", "/"), ("Contact", None)]),
        panel,
        wrap(section_head("Before you write", inc["h2"], inc["intro"], "include-title") + "\n" +
             checklist(inc["bullets"], two_col=True, indent="        "), "include-title", tint=True),
        wrap(section_head("What happens next", nxt["h2"], nxt["intro"], "next-title") + "\n" +
             steps_panel(None, nxt["steps"]), "next-title"),
        faq_section("Questions", "Common questions", "If your question isn't answered here, please contact us by email.",
                    home["faq"], "faq-title"),
    ]
    return "\n\n".join(parts)


def legal_page(eyebrow, h1, p, crumb_label):
    body = []
    for s in p["sections"]:
        body.append(f"          <h2>{t(s['h2'])}</h2>")
        body.append(paras(s["paragraphs"], indent="          "))
    parts = [
        page_hero(eyebrow, h1, p["hero"]["lede"], None, [("Home", "/"), (crumb_label, None)],
                  meta=f"Last updated {UPDATED_HUMAN}"),
        f"""    <section class="section" aria-label="{a(h1)}">
      <div class="container">
        <div class="prose">
{chr(10).join(body)}
        </div>
      </div>
    </section>""",
    ]
    return "\n\n".join(parts)


def not_found_page():
    return page_hero("Not found", "This page could not be found",
                     "The page you were looking for may have moved or may no longer exist. These links may help.",
                     None) + """

    <section class="section" aria-label="Helpful links">
      <div class="container">
        <div class="not-found-links">
          <a class="btn btn-navy" href="/">Home</a>
          <a class="btn btn-navy" href="/services/">Services</a>
          <a class="btn btn-navy" href="/contact/">Contact</a>
        </div>
      </div>
    </section>"""


# --------------------------------------------------------------------------- build

HOME_CONTACT = {}


def out_path(path):
    if path.endswith("/"):
        return ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    return ROOT / path.lstrip("/")


def main():
    home = json.loads((CONTENT / "home.json").read_text(encoding="utf-8"))
    pages = json.loads((CONTENT / "pages.json").read_text(encoding="utf-8"))
    HOME_CONTACT.update(home["contact"])
    site = {"topbar": home["topbar"], "footerAbout": home["footerAbout"]}

    built = []

    def emit(path, title, description, active, main_html, in_sitemap=True):
        html = document(path if in_sitemap else None, title, description, active, main_html, site)
        target = out_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8", newline="\n")
        if in_sitemap:
            built.append(path)

    def title_for(label):
        return f"{label} | {COMPANY}"

    emit("/", home["title"], home["metaDescription"], "/", home_page(home, article_entries(pages)))
    emit("/about/", title_for("About"), pages["about"]["metaDescription"], "/about/", about_page(pages["about"]))
    emit("/services/", title_for("Services"), pages["services"]["metaDescription"], "/services/",
         services_page(pages["services"], pages))
    for svc in SERVICES:
        p = pages["service-" + svc["slug"]]
        emit(f"/services/{svc['slug']}/", title_for(svc["name"]), p["metaDescription"], f"/services/{svc['slug']}/",
             service_page(svc, p, pages))
    emit("/approach/", title_for("Approach"), pages["approach"]["metaDescription"], "/approach/",
         approach_page(pages["approach"]))
    emit("/insights/", title_for("Insights"), pages["insights"]["metaDescription"], "/insights/",
         insights_page(pages["insights"], pages))
    for slug in ARTICLES:
        p = pages["article-" + slug]
        emit(f"/insights/{slug}/", title_for(p["hero"]["h1"]), p["metaDescription"], f"/insights/{slug}/",
             article_page(slug, p, pages))
    emit("/careers/", title_for("Careers"), pages["careers"]["metaDescription"], "/careers/",
         careers_page(pages["careers"]))
    emit("/contact/", title_for("Contact"), pages["contact"]["metaDescription"], "/contact/",
         contact_page(pages["contact"], home))
    emit("/privacy/", title_for("Privacy Notice"), pages["privacy"]["metaDescription"], "/privacy/",
         legal_page("Legal", "Website Privacy Notice", pages["privacy"], "Privacy"))
    emit("/terms/", title_for("Terms of Use"), pages["terms"]["metaDescription"], "/terms/",
         legal_page("Legal", "Terms of Use", pages["terms"], "Terms of Use"))
    emit("/404.html", title_for("Page not found"), "The page you were looking for could not be found.", "",
         not_found_page(), in_sitemap=False)

    urls = "\n".join(f"  <url><loc>{SITE_URL}{p}</loc><lastmod>{UPDATED_ISO}</lastmod></url>" for p in built)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8", newline="\n")
    # The upload page under /vcrg-send/ is a separate site on the same domain; keep it out of search results.
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nDisallow: /vcrg-send/\n\nSitemap: {SITE_URL}/sitemap.xml\n",
        encoding="utf-8", newline="\n")
    print(f"Built {len(built)} pages plus 404.html, sitemap.xml and robots.txt")


if __name__ == "__main__":
    main()
