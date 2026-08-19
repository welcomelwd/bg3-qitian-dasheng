#!/usr/bin/env python3
from pathlib import Path
import csv
import io
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
progressions_text = (ROOT / "data/progressions.csv").read_text(encoding="utf-8")
class_desc_text = (ROOT / "data/class_descriptions.csv").read_text(encoding="utf-8")
stats = (ROOT / "src/stats/VictoriousBuddha.txt").read_text(encoding="utf-8")
spec = (ROOT / "data/victorious_buddha.yaml").read_text(encoding="utf-8")
localization = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "src/stats").glob("Localization*.tsv"))
implementation = (ROOT / "data/implementation_status.csv").read_text(encoding="utf-8")
manifest = json.loads((ROOT / "data/uuid_manifest.json").read_text(encoding="utf-8"))
errors = []

rows = list(csv.DictReader(io.StringIO(progressions_text)))
main_l3 = next((r for r in rows if r["Name"] == "QTD_GreatSage_3"), None)
if not main_l3 or "QTD_VictoriousBuddha" not in (main_l3["SubClasses"] or ""):
    errors.append("Main class L3 must expose QTD_VictoriousBuddha in SubClasses")

sub = [r for r in rows if r["Name"].startswith("QTD_VictoriousBuddha_")]
if [int(r["Level"]) for r in sub] != [3, 6, 10]:
    errors.append("Victorious Buddha progression levels must be 3,6,10")
if any(r["ProgressionType"] != "1" for r in sub):
    errors.append("Victorious Buddha rows must use ProgressionType=1")
if len({r["TableUUID"] for r in sub}) != 1 or (sub and sub[0]["TableUUID"] != "7761cb09-7c56-4ff5-b4eb-8860683eed61"):
    errors.append("Victorious Buddha rows must share the planned subclass TableUUID")

class_rows = list(csv.DictReader(io.StringIO(class_desc_text)))
sub_desc = next((r for r in class_rows if r["Name"] == "QTD_VictoriousBuddha"), None)
if not sub_desc:
    errors.append("Missing QTD_VictoriousBuddha ClassDescriptions row")
else:
    if sub_desc.get("ParentUUID") != "db08d3bc-52c1-4141-a7fb-65bc4a2a155f":
        errors.append("Subclass ParentUUID must point to primary Great Sage ClassDescriptions UUID")
    if sub_desc.get("ProgressionTableUUID") != "7761cb09-7c56-4ff5-b4eb-8860683eed61":
        errors.append("Subclass ClassDescriptions ProgressionTableUUID mismatch")

for token in (
    'new entry "QTD_Passive_VictoriousBuddha_StaffFury"',
    'CriticalHitExtraDice(1,MeleeWeaponAttack)',
    'new entry "QTD_Passive_VictoriousBuddha_ImprovedCritical"',
    'using "ImprovedCritical"',
    'new entry "QTD_Passive_VictoriousBuddha_HeavenBreaker"',
    'UnlockSpell(Target_QTD_HeavenBreakingStrike)',
    'new entry "Target_QTD_HeavenBreakingStrike"',
    'using "Target_MainHandAttack"',
    'UseCosts" "ActionPoint:1;QTD_SageQi:2"',
    'DealDamage(2d8,Force,Magical)',
    'ApplyStatus(QTD_STATUS_HEAVEN_BREAK_ARMOR,100,2)',
    'new entry "QTD_STATUS_HEAVEN_BREAK_ARMOR"',
    'data "Boosts" "AC(-2)"',
):
    if token not in stats:
        errors.append(f"Missing subclass Stats token: {token}")

for token in (
    "tech_name: QTD_VictoriousBuddha",
    "progression_type: 1",
    "role: melee_staff_critical",
    "expected_critical_range: 19-20",
    "sage_qi: 2",
    "armor_class_delta: -2",
    "do_not_grant_extra_action: true",
    "do_not_grant_extra_attack_2: true",
):
    if token not in spec:
        errors.append(f"Missing subclass spec token: {token}")

for key in (
    "QTD_VictoriousBuddha_DisplayName",
    "QTD_Passive_VictoriousBuddha_StaffFury_DisplayName",
    "QTD_Passive_VictoriousBuddha_ImprovedCritical_DisplayName",
    "QTD_Passive_VictoriousBuddha_HeavenBreaker_DisplayName",
    "Target_QTD_HeavenBreakingStrike_DisplayName",
    "QTD_STATUS_HEAVEN_BREAK_ARMOR_DisplayName",
):
    if key not in localization:
        errors.append(f"Missing localization key: {key}")

for line in (
    "Subclass,QTD_VictoriousBuddha,V0.3,subclass-progression-draft",
    "Passive,QTD_Passive_VictoriousBuddha_StaffFury,V0.3,verified-critical-dice-pattern-draft",
    "Passive,QTD_Passive_VictoriousBuddha_ImprovedCritical,V0.3,base-passive-aligned",
    "Spell,Target_QTD_HeavenBreakingStrike,V0.3,mainhand-finisher-draft",
    "Status,QTD_STATUS_HEAVEN_BREAK_ARMOR,V0.3,negative-ac-toolkit-gate",
):
    if line not in implementation:
        errors.append(f"Missing implementation status: {line}")

for key in (
    "subclass_victorious_buddha_table_uuid",
    "subclass_victorious_buddha_classdesc_uuid",
    "subclass_victorious_buddha_l3_uuid",
    "subclass_victorious_buddha_l6_uuid",
    "subclass_victorious_buddha_l10_uuid",
    "passive_victorious_staff_fury_uuid",
    "passive_victorious_improved_critical_uuid",
    "passive_victorious_heaven_breaker_uuid",
    "spell_heaven_breaking_strike_uuid",
    "status_heaven_break_armor_uuid",
):
    if key not in manifest.get("uuids", {}):
        errors.append(f"Missing UUID manifest key: {key}")

if errors:
    print("VICTORIOUS BUDDHA VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("VICTORIOUS BUDDHA VALIDATION OK")
print("Validated subclass selection + L3/L6/L10 progression + critical chain + Heaven-Breaking Strike draft.")
print("Runtime readiness: SUBCLASS-WIRED-DRAFT; AC(-2), weapon restriction, icon and combat behavior still require Patch 8 Toolkit testing.")
