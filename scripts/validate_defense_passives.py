#!/usr/bin/env python3
from pathlib import Path
import csv
import io
import sys

ROOT = Path(__file__).resolve().parents[1]
passives = (ROOT / "src" / "stats" / "Passives.txt").read_text(encoding="utf-8")
progressions_text = (ROOT / "data" / "progressions.csv").read_text(encoding="utf-8")
localization = (ROOT / "src" / "stats" / "Localization.tsv").read_text(encoding="utf-8")
implementation = (ROOT / "data" / "implementation_status.csv").read_text(encoding="utf-8")

errors = []

evasion_required = (
    'new entry "QTD_Passive_GreatSageEvasion"',
    'using "Evasion"',
    'data "DisplayName" "QTD_Passive_GreatSageEvasion_DisplayName"',
    'data "Description" "QTD_Passive_GreatSageEvasion_Description"',
)
for item in evasion_required:
    if item not in passives:
        errors.append(f"Missing Great Sage Evasion field: {item}")

diamond_required = (
    'new entry "QTD_Passive_DiamondBody"',
    'Resistance(Slashing, ResistantToNonMagical)',
    'Resistance(Piercing, ResistantToNonMagical)',
    'Resistance(Bludgeoning, ResistantToNonMagical)',
    'Advantage(SavingThrow, Constitution)',
)
for item in diamond_required:
    if item not in passives:
        errors.append(f"Missing Diamond Body field: {item}")

for forbidden in (
    'Resistance(Slashing, Resistant);Resistance(Piercing, Resistant);Resistance(Bludgeoning, Resistant)',
    'Immunity(Prone)',
    'Immunity(Poison',
):
    if forbidden in passives:
        errors.append(f"Defense V0.2 contains forbidden over-scaling pattern: {forbidden}")

rows = list(csv.DictReader(io.StringIO(progressions_text)))
l7 = next((row for row in rows if row["Name"] == "QTD_GreatSage_7"), None)
l9 = next((row for row in rows if row["Name"] == "QTD_GreatSage_9"), None)
if not l7 or "QTD_Passive_GreatSageEvasion" not in l7["PassivesAdded"]:
    errors.append("Level 7 progression must grant QTD_Passive_GreatSageEvasion")
if not l9 or "QTD_Passive_DiamondBody" not in l9["PassivesAdded"]:
    errors.append("Level 9 progression must grant QTD_Passive_DiamondBody")

for key in (
    "QTD_Passive_GreatSageEvasion_DisplayName",
    "QTD_Passive_GreatSageEvasion_Description",
    "QTD_Passive_DiamondBody_DisplayName",
    "QTD_Passive_DiamondBody_Description",
):
    if key not in localization:
        errors.append(f"Missing defense localization key: {key}")

for status_line in (
    "Passive,QTD_Passive_GreatSageEvasion,V0.2,base-passive-aligned",
    "Passive,QTD_Passive_DiamondBody,V0.2,verified-boost-draft",
):
    if status_line not in implementation:
        errors.append(f"Missing defense implementation status: {status_line}")

if errors:
    print("DEFENSE PASSIVE VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("DEFENSE PASSIVE VALIDATION OK")
print("Validated L7 Evasion inheritance and L9 non-magical physical resistance + Constitution save Advantage.")
print("Runtime readiness: BASE-ALIGNED-DRAFT; local Patch 8 Toolkit/game verification still required.")
