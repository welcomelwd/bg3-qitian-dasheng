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

main_rows = [r for r in rows if r["ProgressionType"] == "0"]
subclass_rows = [r for r in rows if r["ProgressionType"] == "1"]
other_types = sorted({r["ProgressionType"] for r in rows} - {"0", "1"})
if other_types:
    errors.append(f"Unexpected ProgressionType values: {other_types}")

levels = [int(r["Level"]) for r in main_rows]
if levels != list(range(1, 13)):
    errors.append(f"Main class progression levels must be 1..12, got {levels}")

main_tables = {r["TableUUID"] for r in main_rows}
if len(main_tables) != 1:
    errors.append(f"All main class levels must share one TableUUID, got {main_tables}")

row_uuids = [r["UUID"] for r in rows]
if len(row_uuids) != len(set(row_uuids)):
    errors.append("Progression row UUIDs must be unique across class and subclasses")

feat_levels = {int(r["Level"]) for r in main_rows if r["AllowImprovement"] == "Yes"}
if feat_levels != {4, 8, 12}:
    errors.append(f"Main class feat levels expected 4,8,12; got {sorted(feat_levels)}")

subclass_tables = {}
for row in subclass_rows:
    subclass_tables.setdefault(row["TableUUID"], []).append(row)
for table_uuid, group in subclass_tables.items():
    group_levels = [int(r["Level"]) for r in group]
    if group_levels != sorted(group_levels):
        errors.append(f"Subclass progression {table_uuid} levels are not sorted: {group_levels}")
    if not group_levels or group_levels[0] < 3:
        errors.append(f"Subclass progression {table_uuid} must start at level 3 or later")
    if any(r["AllowImprovement"] == "Yes" for r in group):
        errors.append(f"Subclass progression {table_uuid} must not duplicate main-class Feat rows")

for prefix in (
    "QTD_VictoriousBuddha_",
    "QTD_SeventyTwoChanges_",
    "QTD_SpiritualStoneMonkey_",
):
    group = [r for r in subclass_rows if r["Name"].startswith(prefix)]
    if [int(r["Level"]) for r in group] != [3, 6, 10]:
        errors.append(f"{prefix.rstrip('_')} progression expected levels 3,6,10")
    if group and len({r["TableUUID"] for r in group}) != 1:
        errors.append(f"{prefix.rstrip('_')} rows must share one TableUUID")

main_l3 = next((r for r in main_rows if r["Level"] == "3"), None)
expected_subclasses = {"QTD_VictoriousBuddha", "QTD_SeventyTwoChanges", "QTD_SpiritualStoneMonkey"}
if not main_l3:
    errors.append("Missing main class L3 progression")
else:
    actual_subclasses = {s for s in (main_l3["SubClasses"] or "").split(";") if s}
    if actual_subclasses != expected_subclasses:
        errors.append(f"Main L3 subclasses mismatch: {sorted(actual_subclasses)}")

if errors:
    print("SPEC VALIDATION FAILED")
    for e in errors:
        print("-", e)
    sys.exit(1)
print("SPEC VALIDATION OK")
print(f"Validated {len(main_rows)} main progression rows, {len(subclass_rows)} subclass rows and {len(manifest['uuids'])} UUIDs.")
