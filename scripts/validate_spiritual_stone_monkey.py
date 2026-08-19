#!/usr/bin/env python3
from pathlib import Path
import csv
import io
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
progressions_text = (ROOT / "data/progressions.csv").read_text(encoding="utf-8")
class_desc_text = (ROOT / "data/class_descriptions.csv").read_text(encoding="utf-8")
stats = (ROOT / "src/stats/SpiritualStoneMonkey.txt").read_text(encoding="utf-8")
spec = (ROOT / "data/spiritual_stone_monkey.yaml").read_text(encoding="utf-8")
localization = (ROOT / "src/stats/Localization_SpiritualStoneMonkey.tsv").read_text(encoding="utf-8")
implementation = (ROOT / "data/spiritual_stone_monkey_status.csv").read_text(encoding="utf-8")
manifest = json.loads((ROOT / "data/spiritual_stone_monkey_uuids.json").read_text(encoding="utf-8"))
errors = []

rows = list(csv.DictReader(io.StringIO(progressions_text)))
main_l3 = next((r for r in rows if r["Name"] == "QTD_GreatSage_3"), None)
if not main_l3 or "QTD_SpiritualStoneMonkey" not in (main_l3["SubClasses"] or ""):
    errors.append("Main class L3 must expose QTD_SpiritualStoneMonkey")

sub = [r for r in rows if r["Name"].startswith("QTD_SpiritualStoneMonkey_")]
if [int(r["Level"]) for r in sub] != [3, 6, 10]:
    errors.append("Spiritual Stone Monkey progression levels must be 3,6,10")
if any(r["ProgressionType"] != "1" for r in sub):
    errors.append("Spiritual Stone Monkey rows must use ProgressionType=1")
if len({r["TableUUID"] for r in sub}) != 1 or (sub and sub[0]["TableUUID"] != "dc1d9370-6736-4197-b805-25b0e00fd355"):
    errors.append("Spiritual Stone Monkey rows must share the planned subclass TableUUID")

class_rows = list(csv.DictReader(io.StringIO(class_desc_text)))
sub_desc = next((r for r in class_rows if r["Name"] == "QTD_SpiritualStoneMonkey"), None)
if not sub_desc:
    errors.append("Missing QTD_SpiritualStoneMonkey ClassDescriptions row")
else:
    if sub_desc.get("ParentUUID") != "db08d3bc-52c1-4141-a7fb-65bc4a2a155f":
        errors.append("Spiritual Stone Monkey ParentUUID mismatch")
    if sub_desc.get("ProgressionTableUUID") != "dc1d9370-6736-4197-b805-25b0e00fd355":
        errors.append("Spiritual Stone Monkey ProgressionTableUUID mismatch")
    if sub_desc.get("PrimaryAbility") != "Wisdom" or sub_desc.get("SpellCastingAbility") != "Wisdom":
        errors.append("Spiritual Stone Monkey must be Wisdom/Wisdom")

required_stats = (
    'new entry "QTD_Passive_SpiritualStoneMonkey_L3"',
    'SpellSaveDC(1)',
    'RollBonus(MeleeSpellAttack,1)',
    'RollBonus(RangedSpellAttack,1)',
    'UnlockSpell(Zone_QTD_SamadhiFire)',
    'new entry "Zone_QTD_SamadhiFire"',
    'using "Zone_BurningHands"',
    'UseCosts" "ActionPoint:1;QTD_SageQi:2"',
    'new entry "Target_QTD_CloudThunderStep"',
    'using "Target_MistyStep"',
    'TargetRadius" "18"',
    'ApplyStatus(SELF,QTD_STATUS_CLOUD_SPELL_MOMENTUM,100,1)',
    'new entry "QTD_STATUS_CLOUD_SPELL_MOMENTUM"',
    'MovementSpeed(3)',
    'new entry "Projectile_QTD_PalmThunder"',
    'using "Projectile_ChromaticOrb_Lightning"',
    'new entry "Projectile_QTD_FiveElements"',
    'using "Projectile_ChromaticOrb_Monk"',
    'Projectile_QTD_FiveElements_Fire',
    'Projectile_QTD_FiveElements_Water',
    'Projectile_QTD_FiveElements_Lightning',
    'Projectile_QTD_FiveElements_Wind',
    'Projectile_QTD_FiveElements_Earth',
    'using "Projectile_ChromaticOrb_Fire_4"',
    'using "Projectile_ChromaticOrb_Cold_4"',
    'using "Projectile_ChromaticOrb_Lightning_4"',
    'using "Projectile_ChromaticOrb_Thunder_4"',
    'using "Projectile_ChromaticOrb_Acid_4"',
)
for token in required_stats:
    if token not in stats:
        errors.append(f"Missing Spiritual Stone Monkey Stats token: {token}")

if stats.count('UseCosts" "ActionPoint:1;QTD_SageQi:3"') != 5:
    errors.append("Five Elements must have exactly five Sage Qi 3 child casts")
if "KiPoint:" in stats or "SpellSlotsGroup:" in stats:
    errors.append("Spiritual Stone Monkey QTD entries must not consume Ki or SpellSlots")
for forbidden in ("ActionResource(ActionPoint", "ExtraAttack_2", "ExtraAttack_3", "RestoreResource(QTD_SageQi"):
    if forbidden in stats:
        errors.append(f"Forbidden action/resource escalation: {forbidden}")

required_spec = (
    "tech_name: QTD_SpiritualStoneMonkey",
    "role: wisdom_immortal_arts",
    "primary_ability: Wisdom",
    "spellcasting_ability: Wisdom",
    "no_spell_slots: true",
    "base_spell: Zone_BurningHands",
    "base_spell: Target_MistyStep",
    "base_spell: Projectile_ChromaticOrb_Lightning",
    "container_base: Projectile_ChromaticOrb_Monk",
    "sage_qi_per_cast: 3",
    "do_not_grant_spell_slots: true",
    "do_not_grant_extra_action: true",
    "do_not_reduce_all_sage_qi_costs: true",
    "no_script_extender_required: true",
)
for token in required_spec:
    if token not in spec:
        errors.append(f"Missing Spiritual Stone Monkey spec token: {token}")

for key in (
    "QTD_SpiritualStoneMonkey_DisplayName",
    "QTD_Passive_SpiritualStoneMonkey_L3_DisplayName",
    "Zone_QTD_SamadhiFire_DisplayName",
    "QTD_Passive_SpiritualStoneMonkey_L6_DisplayName",
    "Target_QTD_CloudThunderStep_DisplayName",
    "QTD_STATUS_CLOUD_SPELL_MOMENTUM_DisplayName",
    "Projectile_QTD_PalmThunder_DisplayName",
    "QTD_Passive_SpiritualStoneMonkey_L10_DisplayName",
    "Projectile_QTD_FiveElements_DisplayName",
):
    if key not in localization:
        errors.append(f"Missing localization key: {key}")

for line in (
    "Subclass,QTD_SpiritualStoneMonkey,V0.3,subclass-wired-draft",
    "Passive,QTD_Passive_SpiritualStoneMonkey_L3,V0.3,verified-spell-boost-pattern-draft",
    "Spell,Zone_QTD_SamadhiFire,V0.3,burning-hands-aligned-draft",
    "Spell,Target_QTD_CloudThunderStep,V0.3,teleport-status-draft",
    "Status,QTD_STATUS_CLOUD_SPELL_MOMENTUM,V0.3,verified-spell-boost-pattern-draft",
    "Spell,Projectile_QTD_PalmThunder,V0.3,chromatic-orb-aligned-draft",
    "SpellContainer,Projectile_QTD_FiveElements,V0.3,resource-container-draft",
):
    if line not in implementation:
        errors.append(f"Missing implementation status: {line}")

for key in (
    "subclass_spiritual_stone_monkey_table_uuid",
    "subclass_spiritual_stone_monkey_classdesc_uuid",
    "subclass_spiritual_stone_monkey_l3_uuid",
    "subclass_spiritual_stone_monkey_l6_uuid",
    "subclass_spiritual_stone_monkey_l10_uuid",
    "passive_spiritual_l3_uuid",
    "passive_spiritual_l6_uuid",
    "passive_spiritual_l10_uuid",
    "spell_samadhi_fire_uuid",
    "spell_cloud_thunder_step_uuid",
    "status_cloud_spell_momentum_uuid",
    "spell_palm_thunder_uuid",
    "five_elements_container_uuid",
):
    if key not in manifest.get("uuids", {}):
        errors.append(f"Missing UUID manifest key: {key}")

if errors:
    print("SPIRITUAL STONE MONKEY VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("SPIRITUAL STONE MONKEY VALIDATION OK")
print("Validated L3 Wisdom casting, L6 cloud/thunder package, and L10 five-element Sage Qi container.")
print("Runtime readiness: SUBCLASS-WIRED-DRAFT; post-teleport SELF status timing and Chromatic Orb child behavior still require Patch 8 Toolkit testing.")
