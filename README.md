# jjk349.github.io

Portfolio of **James Kurtis**, Mechanical Engineering at Cornell University and Cooling
Sub-team Lead for Cornell Racing FSAE.

Live at **https://jjk349.github.io/**

Plain HTML, CSS, and JavaScript with no framework and no build step on GitHub's side.
A small Python script generates the pages from one content file, so adding or editing
a project means changing text in one place.

## Structure

```
_build/
  content.py       All site text: projects, experience, skills, links  <- edit this
  build.py         Generates the HTML pages from content.py
  art/*.svg        Schematic illustrations used on project cards and pages
assets/
  css/style.css    Styles ("cockpit telemetry" theme: graphite / lime)
  js/main.js       Menu, shift-light scroll progress, session clock, reveals, copy email
  img/             Profile photo, favicon, social share image (og.png)
  resume/          James-Kurtis-Resume.pdf
index.html         Home page             (generated)
projects/*.html    Project write-ups     (generated)
resume.html        Resume viewer         (generated)
404.html           Not-found page        (generated)
sitemap.xml        (generated)
```

## Editing

1. Change text in `_build/content.py`.
2. Rebuild the pages:

   ```
   python _build/build.py
   ```

3. Commit and push. GitHub Pages redeploys within a minute or two.

### Publish a project that's "In the garage"

Projects with `"status": "stub"` show a card marked *In the garage / Write-up coming
soon* and have no page. To publish one, change it to `"status": "full"` and add the
fields the full projects use (`readout`, `lede`, `specs`, `stats`, `sections`, `tools`).
Copy an existing full project as a template.

### Add photos to a project

Put images in `assets/img/projects/` and list them in that project's `gallery`:

```python
"gallery": [
    {"src": "assets/img/projects/tbc-layup.jpg", "alt": "Composite layup of the container", "caption": "Wet layup, first panel"},
],
```

### Update the resume

Replace `assets/resume/James-Kurtis-Resume.pdf` with the new PDF, keeping the same
filename.

## Preview locally

```
python -m http.server 8000
```

then open http://localhost:8000.

## Themes

The site uses the **Cockpit telemetry** theme (race-car dash display). The earlier
**Motorsport bold** theme (black / race red / white livery) is saved as the git tag
`theme-motorsport`, so it can be restored at any time.
