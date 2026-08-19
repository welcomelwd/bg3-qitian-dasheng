#!/usr/bin/env python3
from pathlib import Path
import csv
import io
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
passives = (ROOT / "src" / "stats" / "Passives.txt").read_text(encoding="utf-8")
stats = (ROOT / "src" / "stats" / "ThreeHeadsSixArms.txt").read_text(encoding="utf-8")
spec = (ROOT / "data" / "three_heads_six_arms.yaml").read_text(encoding="utf-8")
progressions_text = (ROOT / "data" / "progressions.csv").read_text(encoding="utf-8")
localization = (ROOT / "src" / "stats" / "Localization.tsv").read_text(encoding="utf-8")
implementation = (ROOT / "data" / "implementation_status.csv").read_text(encoding="utf-8")
manifest = json.loads((ROOT / "data" / "uuid_manifest.json").read_text(encoding="utf-8"))

errors = []

required_passive = (
    'new entry "QTD_Passive_ThreeHeadsSixArms"',
    'UnlockSpell(Shout_QTD_ThreeHeadsSixArms)',
)
for item in required_passive:
    if item not in passives:
        errors.append(f"Missing Three Heads passive field: {item}")

required_stats = (
    'new entry "Shout_QTD_ThreeHeadsSixArms"',
    'data "SpellType" "Shout"',
    'data "UseCosts" "BonusActionPoint:1;QTD_SageQi:4"',
    'ApplyStatus(QTD_STATUS_THREE_HEADS_SIX_ARMS,100,3)',
    'new entry "QTD_STATUS_THREE_HEADS_SIX_ARMS"',
    'data "StatusType" "BOOST"',
    'data "StackId" "QTD_THREE_HEADS_SIX_ARMS"',
    'AC(2)',
    'Advantage(SavingThrow,Strength)',
    'Advantage(SavingThrow,Dexterity)',
    'StatusImmunity(SG_Frightened)',
    'data "Passives" "ExtraAttack_2"',
)
for item in required_stats:
    if item not in stats:
        errors.append(f"Missing Three Heads Stats field: {item}")

executable_stats = "\n".join(
    line for line in stats.splitlines()
    if not line.lstrip().startswith("//")
)
for forbidden in (
    'ExtraAttack_3',
    'ActionResource(ActionPoint',
    'ActionPoint:2',
    'BonusActionPoint:2',
    'Advantage(SavingThrow,Constitution)',
    'Advantage(SavingThrow,Intelligence)',
    'Advantage(SavingThrow,Wisdom)',
    'Advantage(SavingThrow,Charisma)',
):
    if forbidden in executable_stats:
        errors.append(f"Forbidden V0.3 over-scaling pattern in executable Stats: {forbidden}")

required_spec = (
    "unlock_level: 10",
    "sage_qi_cost: 4",
    "duration_rounds: 3",
    "extra_attack_chain: ExtraAttack_2",
    "intended_weapon_attacks_per_attack_action: 3",
    "armor_class_bonus: 2",
    "do_not_grant_full_ActionPoint: true",
    "no_script_extender_required: true",
)
for item in required_spec:
    if item not in spec:
        errors.append(f"Missing Three Heads spec field: {item}")

rows = list(csv.DictReader(io.StringIO(progressions_text)))
l10 = next((row for row in rows if row["Name"] == "QTD_GreatSage_10"), None)
if not l10 or "QTD_Passive_ThreeHeadsSixArms" not in l10["PassivesAdded"]:
    errors.append("Level 10 progression must grant QTD_Passive_ThreeHeadsSixArms")

for key in (
    "QTD_Passive_ThreeHeadsSixArms_DisplayName",
    "QTD_Passive_ThreeHeadsSixArms_Description",
    "Shout_QTD_ThreeHeadsSixArms_DisplayName",
    "Shout_QTD_ThreeHeadsSixArms_Description",
    "QTD_STATUS_THREE_HEADS_SIX_ARMS_DisplayName",
    "QTD_STATUS_THREE_HEADS_SIX_ARMS_Description",
):
    if key not in localization:
        errors.append(f"Missing Three Heads localization key: {key}")

for status_line in (
    "Feature,QTD_ThreeHeadsSixArms,V0.3,active-status-draft",
    "Passive,QTD_Passive_ThreeHeadsSixArms,V0.3,unlock-passive-draft",
    "Spell,Shout_QTD_ThreeHeadsSixArms,V0.3,verified-applystatus-draft",
    "Status,QTD_STATUS_THREE_HEADS_SIX_ARMS,V0.3,extraattack2-status-draft",
):
    if status_line not in implementation:
        errors.append(f"Missing Three Heads implementation status: {status_line}")

for manifest_key in ("spell_three_heads_uuid", "status_three_heads_uuid"):
    if manifest_key not in manifest["uuids"]:
        errors.append(f"Missing planning UUID: {manifest_key}")

if errors:
    print("THREE HEADS SIX ARMS VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("THREE HEADS SIX ARMS VALIDATION OK")
print("Validated L10 unlock, Bonus Action + 4 Sage Qi, 3-round BOOST, ExtraAttack_2, AC +2, STR/DEX save Advantage and fear immunity.")
print("Runtime readiness: ACTIVE-STATUS-DRAFT; local Patch 8 ExtraAttack_2 priority/VFX testing still required.")
