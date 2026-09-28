"""
Static site generator for the portfolio. No dependencies beyond Python 3.8+.

    python _build/build.py

Reads _build/content.py and _build/art/*.svg and writes the site into the
repository root (index.html, resume.html, 404.html, projects/*.html,
sitemap.xml). Commit the generated files; GitHub Pages serves them as-is.

Theme: "Cockpit telemetry" (race-car dash display).
"""

import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from content import (  # noqa: E402
    ABOUT, CATEGORIES, DASH_BAR, EDUCATION, EXPERIENCE, GAUGES, INTERESTS, LEADERSHIP,
    PROJECTS, SITE, SKILLS,
)

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Oxanium:wght@400..800"
    "&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400"
    "&family=JetBrains+Mono:wght@400;500;700&display=swap"
)

ICONS = {
    "arrow": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>',
    "back": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12H5M11 6l-6 6 6 6"/></svg>',
    "download": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>',
    "external": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
    "mail": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 7 9 6 9-6"/></svg>',
    "copy": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="1"/><path d="M5 15V5a1 1 0 0 1 1-1h10"/></svg>',
    "linkedin": '<svg class="i i-fill" viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.75h4v11H3v-11Zm6.5 0h3.8v1.5h.06c.53-1 1.83-1.8 3.44-1.8 3.68 0 4.2 2.2 4.2 5.06v6.24h-4v-5.5c0-1.32-.03-3-1.83-3-1.84 0-2.12 1.43-2.12 2.9v5.6h-4v-11Z"/></svg>',
    "doc": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3H6v18h12V7l-4-4Z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>',
}

CAT_NAMES = {c["id"]: c["name"] for c in CATEGORIES}


def num(i):
    return f"{i:02d}"


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def art(name, uid, label=None):
    """Inline an SVG from _build/art, namespacing its ids so several can share a page."""
    svg = (HERE / "art" / f"{name}.svg").read_text(encoding="utf-8").strip()
    prefix = f"{name}-{uid}"
    svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}-{m.group(1)}"', svg)
    svg = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{prefix}-{m.group(1)})", svg)
    if label:
        attrs = f'class="art-svg" role="img" aria-label="{label}"'
    else:
        attrs = 'class="art-svg" aria-hidden="true" focusable="false"'
    return svg.replace("<svg ", f"<svg {attrs} ", 1)


def corners():
    return (
        '<span class="vf tl" aria-hidden="true"></span><span class="vf tr" aria-hidden="true"></span>'
        '<span class="vf bl" aria-hidden="true"></span><span class="vf br" aria-hidden="true"></span>'
    )


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------

def nav(root, home):
    base = "" if home else (root or "./")
    return f"""<header class="nav" data-nav>
  <div class="wrap nav-inner">
    <a class="brand" href="{root or './'}" aria-label="{SITE['name']}, home">
      <span class="brand-mark">JK</span><span class="brand-name">{SITE['name']}<span class="brand-sub"> // telemetry</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-menu">
      <span class="bars" aria-hidden="true"><span></span><span></span></span><span class="sr">Menu</span>
    </button>
    <nav id="nav-menu" class="nav-menu" aria-label="Primary">
      <a href="{base}#work">Work</a>
      <a href="{base}#experience">Experience</a>
      <a href="{base}#about">About</a>
      <a href="{base}#contact">Contact</a>
      <a class="btn btn-sm btn-primary" href="{root}resume.html">R&eacute;sum&eacute;</a>
    </nav>
  </div>
</header>"""


def footer(root):
    return f"""<footer class="footer">
  <div class="sectors" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="wrap footer-inner">
    <span>&copy; <span data-year>2026</span> {SITE['name']}</span>
    <span class="footer-links">
      <a href="mailto:{SITE['email']}">Email</a>
      <a href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn</a>
      <a href="{root}resume.html">R&eacute;sum&eacute;</a>
    </span>
    <a class="to-top" href="#top">Back to top &uarr;</a>
  </div>
</footer>"""


def page(*, title, description, body, root="", path="", home=False, body_class=""):
    leds = "".join("<i></i>" for _ in range(15))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="{SITE['name']}">
<meta name="theme-color" content="#0a0c0b">
<link rel="canonical" href="{SITE['url']}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE['url']}{path}">
<meta property="og:image" content="{SITE['url']}assets/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{root}assets/css/style.css">
<script>document.documentElement.classList.add("js")</script>
<script src="{root}assets/js/main.js" defer></script>
</head>
<body class="{body_class}" id="top">
<a class="skip" href="#main">Skip to content</a>
<div class="shift" aria-hidden="true">{leds}</div>
{nav(root, home)}
<main id="main">
{body}
</main>
{footer(root)}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Home page pieces
# ---------------------------------------------------------------------------

def gauge(g):
    label = f'<p class="g-label">{g["label"]}</p>'
    if g["type"] == "gauge":
        cx, cy, r = 60, 62, 48
        ticks = []
        for k in range(11):
            a = math.radians(180 - k * 18)
            r1, r2 = (36, 42) if k % 5 else (33, 42)
            ticks.append(
                f"M{cx + r1 * math.cos(a):.1f} {cy - r1 * math.sin(a):.1f}"
                f"L{cx + r2 * math.cos(a):.1f} {cy - r2 * math.sin(a):.1f}"
            )
        lit = round(g["fill"] * 100, 1)
        ang = 180 - g["fill"] * 180
        nx = cx + 40 * math.cos(math.radians(ang))
        ny = cy - 40 * math.sin(math.radians(ang))
        arc = f"M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}"
        svg = f"""<svg class="g-svg" viewBox="0 0 120 70" aria-hidden="true" style="--turn:{g['fill'] * 180:.1f}deg">
      <path class="g-track" d="{arc}" pathLength="100"/>
      <path class="g-cut" d="{arc}" pathLength="100" stroke-dasharray="0 {lit} {100 - lit} 100"/>
      <path class="g-lit" d="{arc}" pathLength="100" stroke-dasharray="{lit} 100"/>
      <path class="g-ticks" d="{' '.join(ticks)}"/>
      <line class="g-needle" x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}"/>
      <circle class="g-hub" cx="{cx}" cy="{cy}" r="4"/>
    </svg>"""
        return f"""<div class="g g-arc">
    {label}
    <div class="g-row">{svg}<div><p class="g-value">{g['value']}</p><p class="g-unit">{g['unit']}</p><p class="g-note">{g.get('note', '')}</p></div></div>
  </div>"""
    value = g["value"]
    if value == "auto":
        value = num(len(PROJECTS))
    if g["type"] == "status":
        return f"""<div class="g g-status">
    {label}
    <p class="g-value"><span class="led on" aria-hidden="true"></span>{value}</p>
    <p class="g-unit">{g['unit']}</p>
  </div>"""
    return f"""<div class="g g-digital">
    {label}
    <p class="g-value">{value}</p>
    <p class="g-unit">{g['unit']}</p>
  </div>"""


def hero():
    bar = "".join(f'<span class="db-item"><b>{k}</b> {v}</span>' for k, v in DASH_BAR)
    gauges = "\n  ".join(gauge(g) for g in GAUGES)
    return f"""<section class="hero" aria-labelledby="hero-name">
  <div class="wrap">
    <div class="dash">
      <div class="dash-bar" aria-hidden="true">
        <span class="db-live"><span class="led on"></span>Live</span>
        {bar}
        <span class="db-clock">Session <b data-clock>00:00</b></span>
      </div>
      <div class="dash-grid">
        <div class="hero-copy">
          <p class="eyebrow">{SITE['title']}</p>
          <h1 id="hero-name" class="hero-name"><span class="l1">{SITE['first']}</span><span class="l2">{SITE['last']}<span class="cursor" aria-hidden="true"></span></span></h1>
          <p class="hero-lede">{SITE['lede']}</p>
          <div class="hero-cta">
            <a class="btn btn-primary" href="#work">See the work {ICONS['arrow']}</a>
            <a class="btn btn-ghost" href="{SITE['resume_pdf']}" download>R&eacute;sum&eacute; {ICONS['download']}</a>
          </div>
          <ul class="socials" aria-label="Contact links">
            <li><a href="mailto:{SITE['email']}">{ICONS['mail']}<span>{SITE['email']}</span></a></li>
            <li><a href="{SITE['linkedin']}" target="_blank" rel="noopener">{ICONS['linkedin']}<span>LinkedIn</span></a></li>
          </ul>
        </div>
        <figure class="cam">
          <div class="cam-frame">
            <img src="{SITE['photo']}" alt="Portrait of {SITE['name']}" width="693" height="1145" fetchpriority="high">
            <div class="cam-hud" aria-hidden="true"><span class="cam-rec"><i></i>Rec</span><span>Cam 01 / Onboard</span></div>
            {corners()}
          </div>
          <figcaption><span>{SITE['location']}</span><span>Class of 20{SITE['class_year']}</span></figcaption>
        </figure>
      </div>
      <div class="gauges">
  {gauges}
      </div>
    </div>
  </div>
</section>"""


def trace():
    """A decorative lap trace (speed + brake channels) used as a divider."""
    W, top, span = 1200, 16, 70
    speed_pts, brake_pts = [], []
    prev = None
    for x in range(0, W + 1, 6):
        t = x / W
        s = 0.55 + 0.3 * math.sin(2 * math.pi * 3.2 * t + 0.5) + 0.1 * math.sin(2 * math.pi * 8.1 * t + 1.3)
        y = top + (1 - s) * span
        speed_pts.append(f"{x},{y:.1f}")
        braking = prev is not None and (y - prev) > 1.6
        brake_pts.append(f"{x},{104 if braking else 118}")
        prev = y
    sectors = "".join(
        f'<line class="t-sector s{i}" x1="{x}" y1="6" x2="{x}" y2="122"/>'
        f'<text class="t-label" x="{x + 6}" y="16">S{i}</text>'
        for i, x in ((1, 400), (2, 800))
    )
    return f"""<div class="trace reveal" aria-hidden="true">
  <div class="wrap">
    <div class="trace-head"><span><i class="k-speed"></i>Speed</span><span><i class="k-brake"></i>Brake</span><span class="trace-lap">Lap trace</span></div>
    <svg class="trace-svg" viewBox="0 0 1200 124">
      <path class="t-grid" d="M0 31H1200M0 62H1200M0 93H1200"/>
      {sectors}
      <polyline class="t-brake" points="{' '.join(brake_pts)}" pathLength="1"/>
      <polyline class="t-speed" points="{' '.join(speed_pts)}" pathLength="1"/>
      <line class="t-cursor" x1="0" y1="0" x2="0" y2="124"/>
    </svg>
  </div>
</div>"""


def sec_head(n, kicker, title, hid, intro=None):
    intro_html = f'\n    <p class="sec-intro">{intro}</p>' if intro else ""
    return f"""<header class="sec-head reveal">
    <span class="sec-num" aria-hidden="true"><small>CH</small>{n}</span>
    <div class="sec-titles">
      <p class="kicker">{kicker}</p>
      <h2 id="{hid}" class="sec-title">{title}</h2>
    </div>{intro_html}
  </header>"""


def card(p, index, delay):
    tags = " / ".join(p["tags"])
    n = num(index)
    art_html = art(p["art"], f"card{index}")
    if p["status"] == "full":
        return f"""<a class="card reveal" style="--i:{delay}" href="projects/{p['slug']}.html">
  <div class="card-bar"><span class="led on" aria-hidden="true"></span><span class="card-ch">CH {n}</span><span class="card-tags">{tags}</span></div>
  <div class="card-art">{art_html}</div>
  <div class="card-body">
    <h3 class="card-title">{p['title']}</h3>
    <p class="card-sum">{p['summary']}</p>
    <div class="card-foot"><span class="readout">{p['readout']}</span><span class="card-go">Open {ICONS['arrow']}</span></div>
  </div>
</a>"""
    return f"""<article class="card is-stub reveal" style="--i:{delay}">
  <div class="card-bar"><span class="led pit" aria-hidden="true"></span><span class="card-ch">CH {n}</span><span class="card-tags">{tags}</span></div>
  <div class="card-art">{art_html}<span class="pitboard">In the garage</span></div>
  <div class="card-body">
    <h3 class="card-title">{p['title']}</h3>
    <p class="card-sum">{p.get('summary', '')}</p>
    <div class="card-foot"><span class="readout muted">Write-up coming soon</span></div>
  </div>
</article>"""


def work_sections():
    out = []
    index = 0
    for ci, cat in enumerate(CATEGORIES, start=1):
        items = [p for p in PROJECTS if p["category"] == cat["id"]]
        cards = []
        for di, p in enumerate(items):
            index += 1
            cards.append(card(p, index, di % 3))
        count = f"{len(items)} project" + ("" if len(items) == 1 else "s")
        layout = {1: "grid grid-solo", 2: "grid grid-duo"}.get(len(items), "grid")
        out.append(f"""<section class="section" id="{cat['id']}" aria-labelledby="{cat['id']}-h">
  <div class="wrap">
  {sec_head(num(ci), f"{cat['kicker']} &nbsp;/&nbsp; {count}", cat['name'], cat['id'] + '-h', cat['intro'])}
  <div class="{layout}">
{chr(10).join(cards)}
  </div>
  </div>
</section>""")
    return '<div id="work">\n' + "\n".join(out) + "\n</div>"


def tower_row(pos, e, open_=False):
    pts = "".join(f"<li>{x}</li>" for x in e["points"])
    place = f'<p class="tower-place">{e["place"]}</p>' if e.get("place") else ""
    return f"""<details class="tower-row"{' open' if open_ else ''}>
  <summary>
    <span class="pos">{pos}</span>
    <span class="org">{e['org']}</span>
    <span class="role">{e['role']}</span>
    <span class="dates">{e['dates']}</span>
    <span class="toggle" aria-hidden="true"></span>
  </summary>
  <div class="tower-detail">{place}<ul>{pts}</ul></div>
</details>"""


def experience(n):
    rows = [tower_row(f"P{i}", e, open_=(i == 1)) for i, e in enumerate(EXPERIENCE, start=1)]
    offset = len(EXPERIENCE)
    lead = [tower_row(f"P{offset + i}", e) for i, e in enumerate(LEADERSHIP, start=1)]
    return f"""<section class="section" id="experience" aria-labelledby="exp-h">
  <div class="wrap">
  {sec_head(num(n), "Timing screen &nbsp;/&nbsp; Tap a row for details", "Experience", "exp-h")}
  <div class="tower reveal">
    <div class="tower-head" aria-hidden="true"><span>Pos</span><span>Team</span><span>Role</span><span>Interval</span><span></span></div>
    {''.join(rows)}
    <div class="tower-divider">Leadership</div>
    {''.join(lead)}
  </div>
  </div>
</section>"""


def about(n):
    paras = "".join(
        f'<p class="{"about-lead" if i == 0 else ""}">{t}</p>' for i, t in enumerate(ABOUT)
    )
    interests = "".join(f"<li>{x}</li>" for x in INTERESTS)
    courses = "".join(f"<li>{x}</li>" for x in EDUCATION["courses"])
    skills = "".join(
        f'<div class="skill-group"><h4>{g}</h4><ul class="chips">{"".join(f"<li>{s}</li>" for s in items)}</ul></div>'
        for g, items in SKILLS
    )
    return f"""<section class="section" id="about" aria-labelledby="about-h">
  <div class="wrap">
  {sec_head(num(n), "Driver profile", "About", "about-h")}
  <div class="about-grid">
    <div class="about-copy reveal">
      {paras}
      <h3 class="mini">Off track</h3>
      <ul class="chips chips-soft">{interests}</ul>
    </div>
    <div class="about-side">
      <article class="panel reveal">
        <p class="kicker">Education</p>
        <h3 class="panel-title">{EDUCATION['school']}</h3>
        <p class="panel-sub">{EDUCATION['degree']} &nbsp;&middot;&nbsp; {EDUCATION['minor']}</p>
        <dl class="mini-stats">
          <div><dt>GPA</dt><dd>{EDUCATION['gpa']}</dd></div>
          <div><dt>Graduation</dt><dd>{EDUCATION['grad'].replace('Expected ', '')}</dd></div>
        </dl>
        <details class="courses">
          <summary>Relevant coursework</summary>
          <ul class="chips">{courses}</ul>
        </details>
      </article>
      <article class="panel reveal">
        <p class="kicker">Toolbox</p>
        {skills}
      </article>
    </div>
  </div>
  </div>
</section>"""


def contact(n):
    wave = "".join(f'<i style="--d:{(k * 37) % 11 / 10:.1f}s"></i>' for k in range(28))
    scope = "".join(
        f'<i style="--h:{0.18 + 0.82 * abs(math.sin(k * 0.55) * math.cos(k * 0.17)):.2f};--d:{(k * 53) % 13 / 10:.1f}s"></i>'
        for k in range(44)
    )
    return f"""<section class="contact section" id="contact" aria-labelledby="contact-h">
  <div class="wrap">
    <div class="radio reveal">
      <div class="radio-bar"><span class="led on" aria-hidden="true"></span><span>Pit radio &nbsp;/&nbsp; Channel open</span><span class="wave" aria-hidden="true">{wave}</span></div>
      <div class="radio-body">
        <div class="radio-copy">
        <p class="kicker">CH {num(n)} &nbsp;/&nbsp; Contact</p>
        <h2 id="contact-h" class="contact-title">Let&rsquo;s build something <span class="hl">fast.</span></h2>
        <p class="contact-sub">{SITE['availability']} for summer internships. Email is the quickest way to reach me.</p>
        <div class="contact-actions">
          <a class="btn btn-primary" href="mailto:{SITE['email']}">{ICONS['mail']} Email me</a>
          <button class="btn btn-ghost" type="button" data-copy="{SITE['email']}">{ICONS['copy']} <span class="as-text" data-copy-label>{SITE['email']}</span></button>
          <a class="btn btn-ghost" href="{SITE['linkedin']}" target="_blank" rel="noopener">{ICONS['linkedin']} LinkedIn</a>
          <a class="btn btn-ghost" href="resume.html">{ICONS['doc']} R&eacute;sum&eacute;</a>
        </div>
        </div>
        <div class="scope" aria-hidden="true">
          <div class="scope-head"><span><span class="led on"></span>TX / J. Kurtis</span><span>RX / You</span></div>
          <div class="scope-wave">{scope}</div>
          <div class="scope-foot"><span>{SITE['location']}</span><span>{SITE['email']}</span></div>
        </div>
      </div>
    </div>
  </div>
</section>"""


def build_index():
    n_cats = len(CATEGORIES)
    body = "\n".join([
        hero(),
        trace(),
        work_sections(),
        experience(n_cats + 1),
        about(n_cats + 2),
        contact(n_cats + 3),
    ])
    return page(
        title=f"{SITE['name']} &mdash; Mechanical Engineer",
        description=SITE["description"],
        body=body,
        root="",
        path="",
        home=True,
        body_class="home",
    )


# ---------------------------------------------------------------------------
# Project pages
# ---------------------------------------------------------------------------

def project_page(p, index, prev_p, next_p):
    n = num(index)
    cat = CAT_NAMES[p["category"]]
    specs = "\n".join(f"      <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["specs"])
    tags = "".join(f"<li>{t}</li>" for t in p["tags"])
    stats = ""
    if p.get("stats"):
        cells = "".join(
            f'<div class="stat"><span class="stat-l">{l}</span><span class="stat-v">{v}</span></div>'
            for v, l in p["stats"]
        )
        stats = f'<div class="wrap"><div class="stats reveal">{cells}</div></div>'

    sections = []
    for si, s in enumerate(p["sections"], start=1):
        inner = "".join(f"<p>{b}</p>" for b in s.get("body", []))
        if s.get("list"):
            inner += '<ul class="bullets">' + "".join(f"<li>{x}</li>" for x in s["list"]) + "</ul>"
        sections.append(
            f'<section class="p-section reveal"><h2 class="p-h2"><span>{num(si)}</span>{s["title"]}</h2>{inner}</section>'
        )

    gallery = ""
    if p.get("gallery"):
        figs = "".join(
            f'<figure><img src="../{g["src"]}" alt="{g["alt"]}" loading="lazy">'
            + (f'<figcaption>{g["caption"]}</figcaption>' if g.get("caption") else "")
            + "</figure>"
            for g in p["gallery"]
        )
        gallery = f'<section class="p-section reveal"><h2 class="p-h2"><span>{num(len(sections) + 1)}</span>Gallery</h2><div class="gallery">{figs}</div></section>'

    tools = "".join(f"<li>{t}</li>" for t in p["tools"])

    def pn(q, cls, label):
        if not q:
            return "<span></span>"
        return (
            f'<a class="{cls}" href="{q["slug"]}.html"><small>{label}</small>'
            f'<strong>{q["title"]}</strong></a>'
        )

    body = f"""<article class="project">
  <header class="p-hero">
    <div class="wrap">
      <a class="back" href="../#work">{ICONS['back']} All work</a>
      <div class="p-hero-grid">
        <div>
          <p class="kicker"><span class="led on" aria-hidden="true"></span>{cat} &nbsp;/&nbsp; Project {n}</p>
          <h1 class="p-title">{p['title']}</h1>
          <p class="p-lede">{p['lede']}</p>
          <ul class="chips chips-tags">{tags}</ul>
        </div>
        <span class="p-num" aria-hidden="true"><small>CH</small>{n}</span>
      </div>
      <dl class="readouts">
{specs}
      </dl>
    </div>
  </header>
  <figure class="wrap p-art reveal">
    <div class="p-art-frame">
      <div class="p-art-bar" aria-hidden="true"><span>Fig. {n}</span><span>Schematic &nbsp;/&nbsp; not to scale</span></div>
      {art(p['art'], 'page', label=f"Schematic illustration for {strip_tags(p['title'])}")}
      {corners()}
    </div>
  </figure>
  {stats}
  <div class="wrap p-body">
    <aside class="p-aside reveal">
      <p class="kicker">Tools &amp; skills</p>
      <ul class="chips">{tools}</ul>
    </aside>
    <div class="p-content">
      {''.join(sections)}
      {gallery}
    </div>
  </div>
  <nav class="wrap p-nav" aria-label="More projects">
    {pn(prev_p, 'prev', '&larr; Previous')}
    {pn(next_p, 'next', 'Next up &rarr;')}
  </nav>
</article>"""
    return page(
        title=f"{strip_tags(p['title'])} &mdash; {SITE['name']}",
        description=strip_tags(p["summary"]).replace('"', "&quot;"),
        body=body,
        root="../",
        path=f"projects/{p['slug']}.html",
        body_class="project-page",
    )


# ---------------------------------------------------------------------------
# Resume + 404
# ---------------------------------------------------------------------------

def build_resume():
    pdf = SITE["resume_pdf"]
    body = f"""<section class="page-head">
  <div class="wrap">
    <a class="back" href="./">{ICONS['back']} Home</a>
    <p class="kicker"><span class="led on" aria-hidden="true"></span>R&eacute;sum&eacute; &nbsp;/&nbsp; PDF</p>
    <h1 class="page-title">{SITE['name']}</h1>
    <p class="p-lede">{EDUCATION['degree']}, {EDUCATION['school']} &nbsp;&middot;&nbsp; {SITE['availability']}</p>
    <div class="actions">
      <a class="btn btn-primary" href="{pdf}" download>{ICONS['download']} Download PDF</a>
      <a class="btn btn-ghost" href="{pdf}" target="_blank" rel="noopener">{ICONS['external']} Open in new tab</a>
    </div>
  </div>
</section>
<section class="wrap resume-view">
  <div class="doc-frame" data-pdf>
    <object data="{pdf}#view=FitH&amp;navpanes=0" type="application/pdf" aria-label="{SITE['name']} r&eacute;sum&eacute;">
      <p>Your browser can&rsquo;t show the PDF here. <a href="{pdf}" download>Download it instead.</a></p>
    </object>
    <div class="doc-fallback">
      {ICONS['doc']}
      <p><strong>{SITE['name']} &mdash; R&eacute;sum&eacute;</strong><br>One page, PDF.</p>
      <div class="actions">
        <a class="btn btn-primary" href="{pdf}" target="_blank" rel="noopener">{ICONS['external']} Open PDF</a>
        <a class="btn btn-ghost" href="{pdf}" download>{ICONS['download']} Download</a>
      </div>
    </div>
  </div>
</section>"""
    return page(
        title=f"R&eacute;sum&eacute; &mdash; {SITE['name']}",
        description=f"R&eacute;sum&eacute; of {SITE['name']}, {EDUCATION['degree']} at {EDUCATION['school']}.",
        body=body,
        root="",
        path="resume.html",
        body_class="resume-page",
    )


def build_404():
    body = f"""<section class="page-head dnf">
  <div class="wrap">
    <p class="kicker"><span class="led warn" aria-hidden="true"></span>Error 404 &nbsp;/&nbsp; Signal lost</p>
    <h1 class="dnf-title">DNF</h1>
    <p class="p-lede">This page didn&rsquo;t finish the race. It may have moved, or it never left the garage.</p>
    <div class="actions"><a class="btn btn-primary" href="/">{ICONS['back']} Back to the pits</a></div>
  </div>
</section>"""
    return page(
        title=f"Page not found &mdash; {SITE['name']}",
        description="Page not found.",
        body=body,
        root="/",
        path="404.html",
        body_class="dnf-page",
    )


def build_sitemap(full):
    urls = [SITE["url"], SITE["url"] + "resume.html"] + [
        f"{SITE['url']}projects/{p['slug']}.html" for p in full
    ]
    rows = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{rows}\n</urlset>\n"
    )


def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"  wrote {rel}")


def main():
    # Number projects in display order (category order, then list order).
    ordered = [p for c in CATEGORIES for p in PROJECTS if p["category"] == c["id"]]
    numbers = {p["slug"]: i for i, p in enumerate(ordered, start=1)}
    full = [p for p in ordered if p["status"] == "full"]

    # Remove pages for projects that are no longer "full".
    wanted = {f"{p['slug']}.html" for p in full}
    for old in (ROOT / "projects").glob("*.html"):
        if old.name not in wanted:
            old.unlink()
            print(f"  removed projects/{old.name}")

    write("index.html", build_index())
    for i, p in enumerate(full):
        prev_p = full[i - 1] if i > 0 else None
        next_p = full[i + 1] if i + 1 < len(full) else None
        write(f"projects/{p['slug']}.html", project_page(p, numbers[p["slug"]], prev_p, next_p))
    write("resume.html", build_resume())
    write("404.html", build_404())
    write("sitemap.xml", build_sitemap(full))


if __name__ == "__main__":
    main()
