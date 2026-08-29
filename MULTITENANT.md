# Multi-tenant branding — one repo, 100+ branded demo URLs

The same site serves every customer. A `?c=<slug>` on the URL rebrands the page
to that customer (name, contact, socials, colours, fonts) at load time. No API,
no backend, no per-customer repo.

- Default / your own brand: `https://harishmkavitha.github.io/haloandgrains/`
- A customer: `https://harishmkavitha.github.io/haloandgrains/?c=sunrise-studio`
- Your private list of all demo links: `…/haloandgrains/demos.html`

## How to add a customer (spreadsheet workflow)

1. Open `config/customers.csv` in Excel or Google Sheets.
2. Add one row. Columns:
   `slug, name, phone, whatsapp, email, address, city, instagram, youtube,
   facebook, colorPrimary, colorInk, font, googleFont`
   - `slug` = the short id used in the URL (`?c=slug`) — lowercase, no spaces.
   - `whatsapp` = digits only with country code, e.g. `919000011111`.
   - `colorPrimary` = the accent colour (hex). The light/dark shades are derived
     automatically; you can override with `colorPrimaryBright` / `colorPrimaryDeep`
     columns if you add them.
   - `colorInk` = optional dark background base (hex). Leave blank to keep default.
   - `googleFont` = optional Google Font family name (e.g. `Poppins`); leave blank
     to use the CSS `font` stack. Any blank cell falls back to the `_default` row,
     so nothing is ever missing.
3. Export as CSV (File → Download → .csv), replace `config/customers.csv`, commit
   and push.
4. The **Build customers config** GitHub Action regenerates `config/customers.json`
   automatically. (Or run `python3 build-config.py` locally and commit.)

The `_default` row defines the fallback values (your own studio). Every customer
inherits anything they leave blank.

## What gets rebranded

- Business name — nav, footer, in-copy mentions, page `<title>` and meta.
- Phone / email / address — contact section and footer (text + `tel:` / `mailto:`).
- WhatsApp — every WhatsApp button (number + pre-filled business name).
- Instagram / YouTube / Facebook — footer icons (a social left blank is hidden).
- City — visible mentions across the copy.
- Colours — accent (3 shades) and optional dark background, via CSS variables.
- Font — the whole site's font stack, or a named Google Font.

Photos are **not** per-customer yet — that's the admin-panel piece we deferred
until you pick a storage approach (GitHub API, serverless, or a backend host).

## First-time setup
Enable the config Action once: repo → Settings → Actions → General → Workflow
permissions → **Read and write** → Save. (Same setting the image manifest Action
uses, so if you already did that, you're done.)
