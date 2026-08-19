#!/usr/bin/env python3
from pathlib import Path
import csv
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

matrix_path = ROOT / "data/runtime_validation_matrix.csv"
audit_path = ROOT / "docs/V01_V03_INTEGRATION_AUDIT.md"
progressions_path = ROOT / "data/progressions.csv"
resources_path = ROOT / "data/action_resources.csv"

required_columns = {
    "ID", "Priority", "TargetVersion", "Area", "TechName", "UnlockLevel",
    "Subclass", "ActionCost", "SageQiCost", "RuntimeState", "PrimaryGate",
    "IssueNumber", "ReleaseBlocking",
}

with matrix_path.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

if not rows:
    errors.append("runtime_validation_matrix.csv must not be empty")
else:
    missing_columns = required_columns - set(rows[0].keys())
    if missing_columns:
        errors.append(f"Missing runtime matrix columns: {sorted(missing_columns)}")

ids = [r.get("ID", "") for r in rows]
if len(ids) != len(set(ids)):
    errors.append("Runtime validation matrix IDs must be unique")

for row in rows:
    if row.get("Priority") not in {"P0", "P1", "P2"}:
        errors.append(f"Invalid priority for {row.get('ID')}: {row.get('Priority')}")
    if row.get("ReleaseBlocking") not in {"yes", "conditional", "no"}:
        errors.append(f"Invalid ReleaseBlocking for {row.get('ID')}: {row.get('ReleaseBlocking')}")
    if row.get("Priority") == "P0":
        if row.get("ReleaseBlocking") != "yes":
            errors.append(f"P0 row {row.get('ID')} must be release-blocking=yes")
        if not (row.get("IssueNumber") or "").isdigit():
            errors.append(f"P0 row {row.get('ID')} must reference a numeric issue")

required_tech_names = {
    "QTD_GreatSage",
    "QTD_SageQi",
    "QTD_Passive_MonkeyAgility",
    "QTD_Passive_RuyiMastery",
    "QTD_Passive_CopperHeadIronArm",
    "Target_QTD_SomersaultCloud",
    "Zone_QTD_SeaCalmingStrike",
    "Target_QTD_FieryGoldenEyes",
    "WPN_QTD_RuyiJinguBang",
    "ARM_QTD_GoldenArmor",
    "BOOTS_QTD_CloudWalking",
    "QTD_TransformContainer",
    "Target_QTD_HairClones",
    "WPN_QTD_HairCloneStaff",
    "QTD_ThreeHeadsSixArms",
    "QTD_VictoriousBuddha",
    "QTD_SeventyTwoChanges",
    "QTD_SpiritualStoneMonkey",
    "QTD_FaTianXiangDi",
    "QTD_QitianDasheng",
    "TRUNK_RELEASE_SCOPE",
}
listed_tech_names = {r.get("TechName") for r in rows}
missing_tech_names = required_tech_names - listed_tech_names
if missing_tech_names:
    errors.append(f"Runtime matrix missing required targets: {sorted(missing_tech_names)}")

with resources_path.open(encoding="utf-8-sig", newline="") as f:
    resource_rows = list(csv.DictReader(f))
sage_qi = next((r for r in resource_rows if r.get("Name") == "QTD_SageQi"), None)
if not sage_qi:
    errors.append("Missing QTD_SageQi from action_resources.csv")
elif sage_qi.get("Recovery") != "ShortRest":
    errors.append("QTD_SageQi recovery must remain ShortRest")

with progressions_path.open(encoding="utf-8-sig", newline="") as f:
    progression_rows = list(csv.DictReader(f))
main_rows = [r for r in progression_rows if r.get("ProgressionType") == "0"]
main_l3 = next((r for r in main_rows if r.get("Name") == "QTD_GreatSage_3"), None)
expected_subclasses = {
    "QTD_VictoriousBuddha",
    "QTD_SeventyTwoChanges",
    "QTD_SpiritualStoneMonkey",
}
if not main_l3:
    errors.append("Missing QTD_GreatSage_3 progression row")
else:
    actual_subclasses = {x for x in (main_l3.get("SubClasses") or "").split(";") if x}
    if actual_subclasses != expected_subclasses:
        errors.append(f"L3 subclass set mismatch: {sorted(actual_subclasses)}")

milestones = {}
running_qi = 0
for row in sorted(main_rows, key=lambda r: int(r["Level"])):
    for amount in re.findall(r"ActionResource\(QTD_SageQi,(\d+),0\)", row.get("Boosts") or ""):
        running_qi += int(amount)
    level = int(row["Level"])
    if level in {1, 2, 5, 8, 11}:
        milestones[level] = running_qi
expected_milestones = {1: 2, 2: 3, 5: 4, 8: 5, 11: 6}
if milestones != expected_milestones:
    errors.append(f"Sage Qi progression mismatch: {milestones}, expected {expected_milestones}")

qitian = (ROOT / "data/qitian_dasheng.yaml").read_text(encoding="utf-8")
if "expected_max_at_level_12: 8" not in qitian:
    errors.append("Qitian Dasheng capstone must retain expected L12 Sage Qi max of 8")

action_guards = {
    "data/three_heads_six_arms.yaml": "do_not_grant_full_ActionPoint: true",
    "data/fa_tian_xiang_di.yaml": "do_not_grant_extra_action_point: true",
    "data/qitian_dasheng.yaml": "do_not_grant_extra_action_point: true",
    "data/victorious_buddha.yaml": "do_not_grant_extra_action: true",
    "data/seventy_two_changes.yaml": "no_extra_action_point: true",
    "data/spiritual_stone_monkey.yaml": "do_not_grant_extra_action: true",
}
for rel, token in action_guards.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    if token not in text:
        errors.append(f"Missing action-economy guard in {rel}: {token}")
if "do_not_grant_bonus_action_point: true" not in qitian:
    errors.append("Qitian Dasheng must not grant a BonusActionPoint")

row_by_id = {r.get("ID"): r for r in rows}
placeholder_checks = (
    ("INT-009", ROOT / "src/stats/Weapons.txt", "TODO_TOOLKIT_CLONE_QUARTERSTAFF_TEMPLATE"),
    ("INT-010", ROOT / "src/stats/Armor.txt", "TODO_TOOLKIT_CLONE_ARMOR_PARENT"),
    ("INT-011", ROOT / "src/stats/Armor.txt", "TODO_TOOLKIT_CLONE_BOOTS_PARENT"),
)
for row_id, path, marker in placeholder_checks:
    state = (row_by_id.get(row_id) or {}).get("RuntimeState", "")
    has_marker = marker in path.read_text(encoding="utf-8")
    if state == "toolkit-parent-pending" and not has_marker:
        errors.append(f"{row_id} says parent pending but safe placeholder is missing: {marker}")
    if state != "toolkit-parent-pending" and has_marker:
        errors.append(f"{row_id} no longer says parent pending but placeholder remains: {marker}")

release_row = row_by_id.get("INT-022")
if not release_row or release_row.get("RuntimeState") != "release-policy-pending":
    errors.append("INT-022 must track release policy while main is a forward trunk")

audit = audit_path.read_text(encoding="utf-8")
for token in ("前向 trunk", "V0.4", "V1.0", "P0", "runtime_validation_matrix.csv"):
    if token not in audit:
        errors.append(f"Integration audit missing required release-gate token: {token}")

workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
if "python scripts/validate_integration_audit.py" not in workflow:
    errors.append("GitHub Actions must run validate_integration_audit.py")

if errors:
    print("INTEGRATION AUDIT VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

p0 = sum(1 for r in rows if r["Priority"] == "P0")
p1 = sum(1 for r in rows if r["Priority"] == "P1")
p2 = sum(1 for r in rows if r["Priority"] == "P2")
print("INTEGRATION AUDIT VALIDATION OK")
print(f"Validated {len(rows)} runtime gates: P0={p0}, P1={p1}, P2={p2}.")
print("Release state: NOT RUNTIME-READY until all P0 gates are closed in local Patch 8 Toolkit tests.")
