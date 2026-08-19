#!/usr/bin/env python3
from pathlib import Path
import csv, json, uuid, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
manifest = json.loads((ROOT / "data/uuid_manifest.json").read_text(encoding="utf-8"))
for key, value in manifest["uuids"].items():
    try:
        uuid.UUID(value)
    except Exception:
        errors.append(f"Invalid UUID: {key}={value}")

with (ROOT / "data/progressions.csv").open(encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))
levels = [int(r["Level"]) for r in rows]
if levels != list(range(1, 13)):
    errors.append(f"Progression levels must be 1..12, got {levels}")

tables = {r["TableUUID"] for r in rows}
if len(tables) != 1:
    errors.append(f"All class levels must share one TableUUID, got {tables}")

row_uuids = [r["UUID"] for r in rows]
if len(row_uuids) != len(set(row_uuids)):
    errors.append("Progression row UUIDs must be unique")

feat_levels = {int(r["Level"]) for r in rows if r["AllowImprovement"] == "Yes"}
if feat_levels != {4, 8, 12}:
    errors.append(f"Feat levels expected 4,8,12; got {sorted(feat_levels)}")

if errors:
    print("SPEC VALIDATION FAILED")
    for e in errors:
        print("-", e)
    sys.exit(1)
print("SPEC VALIDATION OK")
print(f"Validated {len(rows)} progression rows and {len(manifest['uuids'])} UUIDs.")
