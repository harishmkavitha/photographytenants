#!/usr/bin/env python3
# Convert config/customers.csv  ->  config/customers.json
# Maintain the CSV in Excel or Google Sheets (File > Download > .csv),
# drop it in config/, then run:  python3 build-config.py
# (or let the GitHub Action do it automatically on push).
import csv, json, os

CSV_PATH  = os.path.join("config", "customers.csv")
JSON_PATH = os.path.join("config", "customers.json")
BOOL_EMPTY = ("", None)

def clean(row):
    return {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k}

with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
    rows = [clean(r) for r in csv.DictReader(f)]

default = {}
customers = {}
for r in rows:
    slug = (r.get("slug") or "").strip()
    if not slug:
        continue
    data = {k: v for k, v in r.items() if k != "slug" and v not in BOOL_EMPTY}
    if slug == "_default":
        default = data
    else:
        customers[slug] = data

out = {"_default": default, "customers": customers}
os.makedirs("config", exist_ok=True)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("Wrote", JSON_PATH, "-", len(customers), "customers")
