#!/usr/bin/env python3
# Rebuild manifest.json + assets/js/images-data.js from whatever is in images/.
# Run locally (python3 build-manifest.py) or let the GitHub Action run it on push.
import os, re, json, datetime

IMAGES_DIR = "images"
IMG_RE = re.compile(r"\.(?:jpe?g|png|webp|gif|avif)$", re.I)
TITLES = {
"wedding-photographers": "Wedding Photographers",
"pre-wedding-photoshoot": "Pre Wedding Photoshoot",
"maternity-and-pregnancy-photographers": "Maternity & Pregnancy Photographers",
"baby-shower-photographers": "Baby Shower Photographers",
"events-photographers": "Events Photographers",
"portfolio-shoot": "Portfolio Shoot",
"product-e-commerce-photographers": "Product & E-Commerce Photographers",
"birthday-photographers": "Birthday Photographers",
"newborn-photography": "Newborn Photography",
"engagement-photographers": "Engagement Photographers",
"family-shoot": "Family Shoot",
"house-warming-ceremony-photographers": "House Warming Ceremony Photographers",
"photo-restoration-service": "Photo Restoration Service",
"post-wedding-photoshoot": "Post Wedding Photoshoot",
"naming-ceremony-photography": "Naming Ceremony Photography",
"upanayana-photography": "Upanayana Photography",
"shastipurthi-photography": "Shastipurthi Photography",
"photo-frames": "Photo Frames",
"album-designers-and-printers": "Album Designers & Printers",
"candid-wedding-photography": "Candid Wedding Photography",
"candid-videographers": "Candid Videographers",
"professional-videography": "Professional Videography",
"corporate-photographers": "Corporate Photographers",
"christian-wedding-photographers": "Christian Wedding Photographers",
"muslim-wedding-photographers": "Muslim Wedding Photographers",
"digital-photo-studio-near-me": "Digital Photo Studio Near Me",
"puberty-function-photographers": "Puberty Function Photographers",
"portrait-photography": "Portrait Photography",
"karizma-album-printing": "Karizma Album Printing",
"drone-photography": "Drone Photography",
"baby-photoshoot": "Baby Photoshoot",
"photographers-near-me": "Photographers Near Me",
"cradle-ceremony": "Cradle Ceremony",
"photographers": "Photographers",
"video-editing-services": "Video Editing Services",
"corporate-video-production": "Corporate Video Production",
"personalized-coffee-mug-printing-service": "Personalized Coffee Mug Printing Service",
"freelance-photographers": "Freelance Photographers",
"canvera-album-design-and-printing": "Canvera Album Design & Printing",
"elements-resort-prewedding-shoot": "Elements Resort Prewedding Shoot",
"baby-photoshoot-places": "Baby Photoshoot Places",
"maternity-photoshoot-places": "Maternity Photoshoot Places",
"anniversary-photoshoot": "Anniversary Photoshoot",
"holy-communion-baptism-photoshoot": "Holy Communion & Baptism Photoshoot",
"indoor-maternity-photoshoot": "Indoor Maternity Photoshoot",
"fashion-photographers": "Fashion Photographers",
"babys-backyard-studio": "Baby's Backyard Studio"
}

def natural_key(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]

def title_from_slug(slug):
    return " ".join(w.capitalize() for w in re.split(r"[-_]+", slug) if w)

cats = []
if os.path.isdir(IMAGES_DIR):
    for slug in sorted(os.listdir(IMAGES_DIR)):
        d = os.path.join(IMAGES_DIR, slug)
        if not os.path.isdir(d):
            continue
        files = sorted((f for f in os.listdir(d) if IMG_RE.search(f)), key=natural_key)
        if files:
            cats.append({"slug": slug, "title": TITLES.get(slug, title_from_slug(slug)), "files": files})

data = {"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(), "categories": cats}
with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
os.makedirs("assets/js", exist_ok=True)
with open("assets/js/images-data.js", "w", encoding="utf-8") as f:
    f.write("window.IMAGES_DATA=" + json.dumps(data, ensure_ascii=False) + ";")
print("Rebuilt manifest:", len(cats), "folders,",
      sum(len(c["files"]) for c in cats), "images")
