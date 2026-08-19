#!/usr/bin/env python3
from pathlib import Path
import csv
import io
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
passives = (ROOT / "src" / "stats" / "Passives.txt").read_text(encoding="utf-8")
spec = (ROOT / "data" / "qitian_dasheng.yaml").read_text(encoding="utf-8")
progressions_text = (ROOT / "data" / "progressions.csv").read_text(encoding="utf-8")
localization = (ROOT / "src" / "stats" / "Localization.tsv").read_text(encoding="utf-8")
implementation = (ROOT / "data" / "implementation_status.csv").read_text(encoding="utf-8")
manifest = json.loads((ROOT / "data" / "uuid_manifest.json").read_text(encoding="utf-8"))

errors = []

entry_marker = 'new entry "QTD_Passive_QitianDasheng"'
if entry_marker not in passives:
    errors.append("Missing QTD_Passive_QitianDasheng")
    capstone = ""
else:
    capstone = passives.split(entry_marker, 1)[1].split("\nnew entry ", 1)[0]

required_capstone = (
    'type "PassiveData"',
    'data "DisplayName" "QTD_Passive_QitianDasheng_DisplayName"',
    'data "Description" "QTD_Passive_QitianDasheng_Description"',
    'data "Properties" "Highlighted"',
    'ActionResource(QTD_SageQi,2,0)',
    'MovementSpeed(3)',
    'StatusImmunity(SG_Charmed)',
    'StatusImmunity(SG_Frightened)',
)
for token in required_capstone:
    if token not in capstone:
        errors.append(f"Missing capstone PassiveData field: {token}")

for forbidden in (
    "UnlockSpell(",
    "ActionResource(ActionPoint",
    "ActionResource(BonusActionPoint",
    "ExtraAttack_2",
    "ExtraAttack_3",
    "RestoreResource(",
):
    if forbidden in capstone:
        errors.append(f"Forbidden capstone power/action pattern: {forbidden}")

required_spec = (
    "feature: QTD_QitianDasheng",
    "passive: QTD_Passive_QitianDasheng",
    "unlock_level: 12",
    "role: capstone_passive",
    "active_spell: none",
    "base_max_before_capstone: 6",
    "bonus_max_from_capstone: 2",
    "expected_max_at_level_12: 8",
    "movement_bonus_m: 3",
    "charm_immunity: true",
    "frightened_immunity: true",
    "do_not_grant_extra_action_point: true",
    "do_not_grant_bonus_action_point: true",
    "do_not_grant_extra_attack_2: true",
    "do_not_grant_extra_attack_3: true",
    "do_not_reset_fa_tian_long_rest_marker: true",
    "do_not_add_new_active_capstone_spell: true",
    "no_script_extender_required: true",
)
for token in required_spec:
    if token not in spec:
        errors.append(f"Missing capstone spec field: {token}")

rows = list(csv.DictReader(io.StringIO(progressions_text)))
l12 = next((row for row in rows if row["Name"] == "QTD_GreatSage_12"), None)
if not l12:
    errors.append("Missing L12 progression row")
else:
    if "QTD_Passive_QitianDasheng" not in l12["PassivesAdded"]:
        errors.append("L12 progression must grant QTD_Passive_QitianDasheng")
    if l12["AllowImprovement"] != "Yes":
        errors.append("L12 must retain its Feat / AllowImprovement=Yes")
    if l12["Boosts"]:
        errors.append("L12 resource increase must live in capstone passive, not duplicate in Progression Boosts")

base_qi = 0
for row in rows:
    level = int(row["Level"])
    if level >= 12:
        continue
    for amount in re.findall(r"ActionResource\(QTD_SageQi,([0-9]+),0\)", row["Boosts"] or ""):
        base_qi += int(amount)
if base_qi != 6:
    errors.append(f"Expected pre-capstone Sage Qi capacity contributions to total 6, got {base_qi}")

for key in (
    "QTD_Passive_QitianDasheng_DisplayName",
    "QTD_Passive_QitianDasheng_Description",
):
    if key not in localization:
        errors.append(f"Missing capstone localization key: {key}")

for line in (
    "Feature,QTD_QitianDasheng,V1.0,capstone-passive-draft",
    "Passive,QTD_Passive_QitianDasheng,V1.0,verified-boost-pattern-draft",
):
    if line not in implementation:
        errors.append(f"Missing capstone implementation status: {line}")

if "passive_qitian_uuid" not in manifest.get("uuids", {}):
    errors.append("Missing passive_qitian_uuid planning UUID")

if errors:
    print("QITIAN DASHENG CAPSTONE VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("QITIAN DASHENG CAPSTONE VALIDATION OK")
print("Validated L12 passive capstone: Sage Qi 6->8, +3m Movement, Charmed/Frightened immunity, retained Feat, and no new action-economy escalation.")
print("Runtime readiness: VERIFIED-BOOST-PATTERN-DRAFT; local Patch 8 Toolkit validation still required for resource cap stacking and status-group coverage.")
