"""
Static site generator for the portfolio. No dependencies beyond Python 3.8+.

    python _build/build.py

Reads _build/content.py and _build/art/*.svg and writes the site into the
repository root (index.html, resume.html, 404.html, projects/*.html,
sitemap.xml). Commit the generated files; GitHub Pages serves them as-is.

Theme: "Minimal" (light, one red accent, interactive animations).
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from content import (  # noqa: E402
    ABOUT, ABOUT_PHOTO, CATEGORIES, EDUCATION, EXPERIENCE, FACTS, INTERESTS, LEADERSHIP,
    PROJECTS, SITE, SKILLS,
)

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Inter+Tight:wght@400;500;600;700"
    "&family=Inter:wght@400;500"
    "&family=JetBrains+Mono:wght@400;500&display=swap"
)

ICONS = {
    "arrow": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>',
    "arrow-ne": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
    "back": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12H5M11 6l-6 6 6 6"/></svg>',
    "download": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>',
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
        attrs = f'class="art-svg" data-draw role="img" aria-label="{label}"'
    else:
        attrs = 'class="art-svg" data-draw aria-hidden="true" focusable="false"'
    return svg.replace("<svg ", f"<svg {attrs} ", 1)


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------

def nav(root, home):
    base = "" if home else (root or "./")
    return f"""<header class="nav" data-nav>
  <div class="wrap nav-inner">
    <a class="brand" href="{root or './'}" aria-label="{SITE['name']}, home">
      <span class="brand-mark" aria-hidden="true"></span>{SITE['name']}
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-menu">
      <span class="bars" aria-hidden="true"><span></span><span></span></span><span class="sr">Menu</span>
    </button>
    <nav id="nav-menu" class="nav-menu" aria-label="Primary">
      <a href="{base}#about">About</a>
      <a href="{base}#work">Projects</a>
      <a href="{base}#experience">Experience</a>
      <a href="{base}#contact">Contact</a>
      <a class="btn btn-sm btn-outline" href="{root}resume.html">R&eacute;sum&eacute;</a>
    </nav>
  </div>
</header>"""


def footer(root):
    return f"""<footer class="footer">
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
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="{SITE['name']}">
<meta name="theme-color" content="#fafaf8">
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
<div class="progress" aria-hidden="true"><span></span></div>
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

def hero():
    facts = "\n".join(f"      <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in FACTS)
    return f"""<section class="hero" aria-labelledby="hero-name">
  <div class="wrap">
    <div class="hero-grid">
      <div class="hero-copy">
        <p class="eyebrow"><span class="dot" aria-hidden="true"></span>{SITE['title']}</p>
        <h1 id="hero-name" class="hero-name"><span class="line"><span>{SITE['first']}</span></span><span class="line"><span>{SITE['last']}</span></span></h1>
        <p class="hero-lede">{SITE['lede']}</p>
        <div class="hero-cta">
          <a class="btn btn-solid" href="#work">See my work {ICONS['arrow']}</a>
          <a class="btn btn-outline" href="{SITE['resume_pdf']}" download>Download r&eacute;sum&eacute; {ICONS['download']}</a>
        </div>
        <ul class="socials" aria-label="Contact links">
          <li><a href="mailto:{SITE['email']}">{ICONS['mail']}<span>{SITE['email']}</span></a></li>
          <li><a href="{SITE['linkedin']}" target="_blank" rel="noopener">{ICONS['linkedin']}<span>LinkedIn</span></a></li>
        </ul>
      </div>
      <figure class="framed hero-photo">
        <div class="photo-frame"><img src="{SITE['photo']}" alt="Portrait of {SITE['name']}" width="693" height="1145" fetchpriority="high"></div>
      </figure>
    </div>
    <dl class="facts">
{facts}
    </dl>
  </div>
</section>"""


def sec_head(n, kicker, title, hid, intro=None):
    intro_html = f'\n    <p class="sec-intro">{intro}</p>' if intro else ""
    return f"""<header class="sec-head reveal">
    <div class="sec-titles">
      <p class="kicker"><span class="sec-num">{n}</span>{kicker}</p>
      <h2 id="{hid}" class="sec-title">{title}</h2>
    </div>{intro_html}
  </header>"""


def card(p, index, delay):
    tags = " &middot; ".join(p["tags"])
    n = num(index)
    art_html = art(p["art"], f"card{index}")
    if p["status"] == "full":
        return f"""<a class="card reveal" style="--i:{delay}" href="projects/{p['slug']}.html">
  <div class="card-art">{art_html}</div>
  <div class="card-body">
    <p class="card-meta"><span class="card-num">{n}</span><span>{tags}</span></p>
    <h3 class="card-title">{p['title']}</h3>
    <p class="card-sum">{p['summary']}</p>
    <div class="card-foot"><span class="readout">{p['readout']}</span><span class="card-go">Read {ICONS['arrow']}</span></div>
  </div>
</a>"""
    return f"""<article class="card is-stub reveal" style="--i:{delay}">
  <div class="card-art">{art_html}<span class="soon"><span class="dot" aria-hidden="true"></span>In progress</span></div>
  <div class="card-body">
    <p class="card-meta"><span class="card-num">{n}</span><span>{tags}</span></p>
    <h3 class="card-title">{p['title']}</h3>
    <p class="card-sum">{p.get('summary', '')}</p>
    <div class="card-foot"><span class="readout muted">Write-up coming soon</span></div>
  </div>
</article>"""


def projects(n):
    subs = []
    index = 0
    for cat in CATEGORIES:
        items = [p for p in PROJECTS if p["category"] == cat["id"]]
        cards = []
        for di, p in enumerate(items):
            index += 1
            cards.append(card(p, index, di % 3))
        count = f"{len(items)} project" + ("" if len(items) == 1 else "s")
        layout = {1: "grid grid-solo", 2: "grid grid-duo"}.get(len(items), "grid")
        sub_intro = f'\n        <p class="sub-intro">{cat["intro"]}</p>' if cat.get("intro") else ""
        subs.append(f"""<div class="subsection" id="{cat['id']}">
    <header class="sub-head reveal">
      <div>
        <h3 class="sub-title">{cat['name']}</h3>{sub_intro}
      </div>
      <span class="sub-count">{count}</span>
    </header>
    <div class="{layout}">
{chr(10).join(cards)}
    </div>
  </div>""")
    total = f"{len(PROJECTS)} projects"
    intro = "Open a project for the full write-up."
    return f"""<section class="section" id="work" aria-labelledby="work-h">
  <div class="wrap">
  {sec_head(num(n), total, "My Projects", "work-h", intro)}
  {chr(10).join(subs)}
  </div>
</section>"""


def acc_row(e, open_=False):
    pts = "".join(f"<li>{x}</li>" for x in e["points"])
    place = f'<p class="acc-place">{e["place"]}</p>' if e.get("place") else ""
    return f"""<details class="acc"{' open' if open_ else ''}>
  <summary>
    <span class="org">{e['org']}</span>
    <span class="role">{e['role']}</span>
    <span class="dates">{e['dates']}</span>
    <span class="toggle" aria-hidden="true"></span>
  </summary>
  <div class="acc-body">{place}<ul>{pts}</ul></div>
</details>"""


def experience(n):
    rows = "".join(acc_row(e, open_=(i == 0)) for i, e in enumerate(EXPERIENCE))
    lead = "".join(acc_row(e) for e in LEADERSHIP)
    return f"""<section class="section" id="experience" aria-labelledby="exp-h">
  <div class="wrap">
  {sec_head(num(n), "Click a role for details", "Experience", "exp-h")}
  <div class="exp reveal">
    <div class="exp-group">{rows}</div>
    <p class="exp-label">Leadership</p>
    <div class="exp-group">{lead}</div>
  </div>
  </div>
</section>"""


def about_me(n):
    paras = "".join(
        f'<p class="{"about-lead" if i == 0 else ""}">{t}</p>' for i, t in enumerate(ABOUT)
    )
    interests = "".join(f"<li>{x}</li>" for x in INTERESTS)
    return f"""<section class="section about-me" id="about" aria-labelledby="about-h">
  <div class="wrap">
    <div class="about-me-grid">
      <div class="about-copy reveal">
        <p class="kicker"><span class="sec-num">{num(n)}</span>Introduction</p>
        <h2 id="about-h" class="sec-title">About Me</h2>
        {paras}
        <p class="mini">Outside of engineering</p>
        <ul class="chips">{interests}</ul>
      </div>
      <figure class="framed about-photo reveal">
        <div class="photo-frame"><img src="{ABOUT_PHOTO['src']}" alt="{ABOUT_PHOTO['alt']}" width="960" height="1280" loading="lazy"></div>
      </figure>
    </div>
  </div>
</section>"""


def education_skills(n):
    courses = "".join(f"<li>{x}</li>" for x in EDUCATION["courses"])
    skills = "".join(
        f'<div class="skill-group"><h4>{g}</h4><ul class="chips">{"".join(f"<li>{s}</li>" for s in items)}</ul></div>'
        for g, items in SKILLS
    )
    return f"""<section class="section" id="skills" aria-labelledby="skills-h">
  <div class="wrap">
  {sec_head(num(n), "Background", "Education &amp; Skills", "skills-h")}
  <div class="edu-grid">
    <article class="panel reveal">
      <p class="mini">Education</p>
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
    <article class="panel reveal" style="--i:1">
      <p class="mini">Tools &amp; skills</p>
      {skills}
    </article>
  </div>
  </div>
</section>"""


def contact(n):
    return f"""<section class="section contact" id="contact" aria-labelledby="contact-h">
  <div class="wrap">
    <div class="contact-inner reveal">
      <p class="kicker"><span class="sec-num">{num(n)}</span>Contact</p>
      <h2 id="contact-h" class="contact-title">Get in <span class="hl">touch</span></h2>
      <p class="contact-sub">{SITE['availability']} for summer internships. Email is the quickest way to reach me.</p>
      <a class="big-mail" href="mailto:{SITE['email']}">{SITE['email']} {ICONS['arrow-ne']}</a>
      <div class="contact-actions">
        <button class="btn btn-outline" type="button" data-copy="{SITE['email']}">{ICONS['copy']} <span data-copy-label>Copy email</span></button>
        <a class="btn btn-outline" href="{SITE['linkedin']}" target="_blank" rel="noopener">{ICONS['linkedin']} LinkedIn</a>
        <a class="btn btn-outline" href="resume.html">{ICONS['doc']} R&eacute;sum&eacute;</a>
      </div>
    </div>
  </div>
</section>"""


def build_index():
    body = "\n".join([
        hero(),
        about_me(1),
        projects(2),
        experience(3),
        education_skills(4),
        contact(5),
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
            f'<div class="stat"><span class="stat-v">{v}</span><span class="stat-l">{l}</span></div>'
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
      <a class="back" href="../#work">{ICONS['back']} All projects</a>
      <p class="kicker"><span class="sec-num">{n}</span>{cat}</p>
      <h1 class="p-title">{p['title']}</h1>
      <p class="p-lede">{p['lede']}</p>
      <ul class="chips chips-tags">{tags}</ul>
      <dl class="facts">
{specs}
      </dl>
    </div>
  </header>
  <figure class="wrap p-art reveal">
    <div class="p-art-frame">{art(p['art'], 'page', label=f"Schematic illustration for {strip_tags(p['title'])}")}</div>
    <figcaption>Fig. {n} &nbsp;&middot;&nbsp; Schematic illustration, not to scale</figcaption>
  </figure>
  {stats}
  <div class="wrap p-body">
    <aside class="p-aside reveal">
      <p class="mini">Tools &amp; skills</p>
      <ul class="chips">{tools}</ul>
    </aside>
    <div class="p-content">
      {''.join(sections)}
      {gallery}
    </div>
  </div>
  <nav class="wrap p-nav" aria-label="More projects">
    {pn(prev_p, 'prev', '&larr; Previous')}
    {pn(next_p, 'next', 'Next &rarr;')}
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
    <p class="kicker">R&eacute;sum&eacute;</p>
    <h1 class="page-title">{SITE['name']}</h1>
    <p class="p-lede">{EDUCATION['degree']}, {EDUCATION['school']} &nbsp;&middot;&nbsp; {SITE['availability']}</p>
    <div class="actions">
      <a class="btn btn-solid" href="{pdf}" download>{ICONS['download']} Download PDF</a>
      <a class="btn btn-outline" href="{pdf}" target="_blank" rel="noopener">{ICONS['arrow-ne']} Open in new tab</a>
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
        <a class="btn btn-solid" href="{pdf}" target="_blank" rel="noopener">{ICONS['arrow-ne']} Open PDF</a>
        <a class="btn btn-outline" href="{pdf}" download>{ICONS['download']} Download</a>
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
    <p class="kicker">Error 404</p>
    <h1 class="dnf-title">Page not found</h1>
    <p class="p-lede">This page may have moved, or it never left the garage.</p>
    <div class="actions"><a class="btn btn-solid" href="/">{ICONS['back']} Back to home</a></div>
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
