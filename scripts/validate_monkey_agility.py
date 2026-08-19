#!/usr/bin/env python3
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

passives = (ROOT / "src/stats/Passives.txt").read_text(encoding="utf-8")
with (ROOT / "data/progressions.csv").open(encoding="utf-8-sig", newline="") as f:
    progressions = list(csv.DictReader(f))
with (ROOT / "data/runtime_validation_matrix.csv").open(encoding="utf-8-sig", newline="") as f:
    matrix = list(csv.DictReader(f))

required = [
    'new entry "QTD_Passive_MonkeyAgility"',
    'data "Boosts" "ACOverrideFormula(10,true,Dexterity,Wisdom)"',
    'data "BoostContext" "OnEquip;OnCreate"',
    'data "BoostConditions" "not WearingArmor(context.Source) and not HasShieldEquipped(context.Source)"',
    'new entry "QTD_Passive_MonkeyAgility_Mobility"',
    'data "Properties" "IsHidden"',
    'ActionResource(Movement,3,0)',
    'JumpMaxDistanceMultiplier(1.5)',
    'FallDamageMultiplier(0.5)',
]
for token in required:
    if token not in passives:
        errors.append(f"Missing Monkey Agility token: {token}")

if 'MovementSpeed(3)' in passives.split('new entry "QTD_Passive_RuyiMastery"')[0]:
    errors.append("Monkey Agility must not use MovementSpeed(3); use ActionResource(Movement,3,0)")

l1 = next((r for r in progressions if r.get("Name") == "QTD_GreatSage_1"), None)
if not l1:
    errors.append("Missing QTD_GreatSage_1")
else:
    added = set((l1.get("PassivesAdded") or "").split(";"))
    for name in ("QTD_Passive_MonkeyAgility", "QTD_Passive_MonkeyAgility_Mobility"):
        if name not in added:
            errors.append(f"L1 must grant {name}")

row = next((r for r in matrix if r.get("ID") == "INT-003"), None)
if not row or row.get("RuntimeState") != "vanilla-pattern-aligned-draft":
    errors.append("INT-003 must be vanilla-pattern-aligned-draft until Toolkit runtime validation")

workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
if "python scripts/validate_monkey_agility.py" not in workflow:
    errors.append("GitHub Actions must run validate_monkey_agility.py")

if errors:
    print("MONKEY AGILITY VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("MONKEY AGILITY VALIDATION OK")
print("Validated unarmoured AC, hidden mobility helper, and 50% fall-damage draft.")
print("Runtime readiness: PENDING PATCH 8 TOOLKIT ARMOUR/SHIELD/FALL TESTS.")
