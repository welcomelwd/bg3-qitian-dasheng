#!/usr/bin/env python3
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

passives = (ROOT / "src/stats/Passives.txt").read_text(encoding="utf-8")
weapons = (ROOT / "src/stats/Weapons.txt").read_text(encoding="utf-8")
spec = (ROOT / "data/passives.yaml").read_text(encoding="utf-8")
refs = (ROOT / "data/reference_patterns_ruyi_mastery.yaml").read_text(encoding="utf-8")
doc = (ROOT / "docs/V01_RUYI_MASTERY.md").read_text(encoding="utf-8")
workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

start = passives.find('new entry "QTD_Passive_RuyiMastery"')
end = passives.find('new entry "QTD_Passive_CopperHeadIronArm"', start)
if start < 0 or end < 0:
    errors.append("Could not isolate QTD_Passive_RuyiMastery entry")
    ruyi = ""
else:
    ruyi = passives[start:end]

required_passive_tokens = (
    'data "BoostConditions" "IsDexterityGreaterThanStrength()"',
    'data "Boosts" "MonkWeaponAttackOverride()"',
    'OnEquip',
    'OnCreate',
    'OnInventoryChanged',
    'OnStatusApply',
    'OnStatusRemove',
)
for token in required_passive_tokens:
    if token not in ruyi:
        errors.append(f"Ruyi Mastery missing required token: {token}")

for forbidden in (
    'WeaponAttackRollAbilityOverride(Dexterity)',
    'WeaponProperty(Finesse)',
    'Finesse',
):
    if forbidden in ruyi:
        errors.append(f"Ruyi Mastery must not hard-force DEX/Finesse: {forbidden}")

if "TODO_TOOLKIT_VERIFY_FINESSE" in weapons:
    errors.append("Weapons.txt still contains obsolete Finesse TODO")
if "MonkWeaponAttackOverride()" not in weapons:
    errors.append("Weapons.txt must document Ruyi Mastery as the Jingu Bang ability-selection path")

for token in (
    "runtime_state: monk-weapon-pattern-aligned-draft",
    "dexterity_gate: IsDexterityGreaterThanStrength()",
    "attack_override: MonkWeaponAttackOverride()",
    "WPN_QTD_RuyiJinguBang",
):
    if token not in spec:
        errors.append(f"passives.yaml missing Ruyi token: {token}")

for token in (
    "CL_Passive_OneDnD_MartialArts_DextrousAttacks",
    "IsDexterityGreaterThanStrength()",
    "MonkWeaponAttackOverride()",
    "WeaponAttackRollAbilityOverride(Dexterity)",
):
    if token not in refs:
        errors.append(f"reference pattern file missing: {token}")

with (ROOT / "data/runtime_validation_matrix.csv").open(encoding="utf-8-sig", newline="") as f:
    matrix = list(csv.DictReader(f))
row = next((r for r in matrix if r.get("ID") == "INT-004"), None)
if not row:
    errors.append("INT-004 missing from runtime validation matrix")
elif row.get("RuntimeState") != "monk-weapon-pattern-aligned-draft":
    errors.append(f"INT-004 RuntimeState mismatch: {row.get('RuntimeState')}")

with (ROOT / "data/implementation_status.csv").open(encoding="utf-8-sig", newline="") as f:
    statuses = list(csv.DictReader(f))
row = next((r for r in statuses if r.get("TechName") == "QTD_Passive_RuyiMastery"), None)
if not row or row.get("Status") != "monk-weapon-pattern-aligned-draft":
    errors.append("implementation_status.csv must mark Ruyi Mastery monk-weapon-pattern-aligned-draft")

with (ROOT / "data/progressions.csv").open(encoding="utf-8-sig", newline="") as f:
    progressions = list(csv.DictReader(f))
l1 = next((r for r in progressions if r.get("Name") == "QTD_GreatSage_1" and r.get("ProgressionType") == "0"), None)
if not l1 or "QTD_Passive_RuyiMastery" not in (l1.get("PassivesAdded") or ""):
    errors.append("L1 progression must grant QTD_Passive_RuyiMastery")

for token in (
    "STR 16 / DEX 12",
    "STR 12 / DEX 16",
    "WPN_QTD_RuyiJinguBang",
    "非 Quarterstaff",
    "toolkit-verified",
):
    if token not in doc:
        errors.append(f"Ruyi runtime document missing test token: {token}")

if "python scripts/validate_ruyi_mastery.py" not in workflow:
    errors.append("GitHub Actions must run validate_ruyi_mastery.py")

if errors:
    print("RUYI MASTERY VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("RUYI MASTERY VALIDATION OK")
print("Validated conditional DEX>STR MonkWeaponAttackOverride path without blanket Finesse or unconditional DEX override.")
print("Runtime readiness: PENDING PATCH 8 TOOLKIT QUARTERSTAFF/JINGU/CONTROL-WEAPON TESTS.")
