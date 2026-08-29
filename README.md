# Halo & Grain — photography & videography website

Static multi-page site (plain HTML/CSS/JS, no build step) for GitHub Pages.
Images are loaded **dynamically** from the site's own `images/` folder — add,
rename or delete a photo and the site keeps working, with no blank boxes.

## How the dynamic gallery works
1. Put photos in `images/<service-slug>/` (one subfolder per service — the
   slugs match the service page filenames in `services/`).
2. On every push that touches `images/**`, the GitHub Action
   (`.github/workflows/build-manifest.yml`) runs `build-manifest.py`, which
   rescans `images/` and rewrites `manifest.json` + `assets/js/images-data.js`.
3. In the browser, `assets/js/gallery.js` fetches `manifest.json` and renders
   every gallery, hero and thumbnail from it. Each `<img>` has an error guard,
   so a just-deleted / renamed file is never shown as a broken image.

So: **you only ever add/remove files in `images/<slug>/` and push.** No lists to
maintain by hand, no API, no cost.

### First-time setup (one time)
- Enable the Action: repo *Settings -> Actions -> General -> Workflow
  permissions -> Read and write*, then push once (or run the workflow manually).
- Or skip Actions entirely and run `python3 build-manifest.py` locally whenever
  you change images, then commit the regenerated `manifest.json`.

### Folder -> service slugs
Each folder name must match a service page, e.g. `images/wedding-photographers/`,
`images/newborn-photography/`, `images/drone-photography/`. Full list is in
`manifest.json`.

## Before launch
- Replace `https://example.com` with your real domain (canonical/OG/sitemap).
- Replace the placeholder phone / email / studio address (keep them identical
  to your Google Business Profile).
- Finish the `privacy.html` / `terms.html` drafts (add a real grievance officer).

## Regenerate the pages themselves
`gen.py` (kept in this archive) builds all the HTML pages. Run `python3 gen.py`
after editing copy. It does **not** touch `images/` — that stays yours.
