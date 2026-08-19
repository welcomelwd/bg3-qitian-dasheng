#!/usr/bin/env python3
from pathlib import Path
import csv
import io
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = (ROOT / "data" / "hair_clones.yaml").read_text(encoding="utf-8")
spells = (ROOT / "src" / "stats" / "HairClones.txt").read_text(encoding="utf-8")
statuses = (ROOT / "src" / "stats" / "HairCloneStatuses.txt").read_text(encoding="utf-8")
characters = (ROOT / "src" / "stats" / "HairCloneCharacters.txt").read_text(encoding="utf-8")
spell_lists_text = (ROOT / "data" / "spell_lists.csv").read_text(encoding="utf-8")

TIERS = [
    {"levels": "6-7", "root": "8c17bf83-fc1d-4143-b555-46b38003bb49", "character": "QTD_HairCloneCharacter_L6", "level": "6", "hp": "24", "ac": "14", "condition": "not ClassLevelHigherOrEqualThan(8,'QTD_GreatSage')"},
    {"levels": "8-9", "root": "122996e7-46e1-4f04-b64d-30db7c9a47ac", "character": "QTD_HairCloneCharacter_L8", "level": "8", "hp": "32", "ac": "15", "condition": "ClassLevelHigherOrEqualThan(8,'QTD_GreatSage') and not ClassLevelHigherOrEqualThan(10,'QTD_GreatSage')"},
    {"levels": "10-11", "root": "72fdc168-2ec4-45ed-a230-21df703ff6c0", "character": "QTD_HairCloneCharacter_L10", "level": "10", "hp": "40", "ac": "16", "condition": "ClassLevelHigherOrEqualThan(10,'QTD_GreatSage') and not ClassLevelHigherOrEqualThan(12,'QTD_GreatSage')"},
    {"levels": "12", "root": "b3368e82-088a-46fb-b8ec-dbc5dc5d4fe0", "character": "QTD_HairCloneCharacter_L12", "level": "12", "hp": "48", "ac": "17", "condition": "ClassLevelHigherOrEqualThan(12,'QTD_GreatSage')"},
]

errors = []

required_spec = (
    "spell: Target_QTD_HairClones",
    "unlock_level: 6",
    "sage_qi_cost: 3",
    "summon_count: 2",
    "lifetime_rounds: 3",
    "use_caster_passives: true",
    "scaling_mode: fixed_templates_by_class_level",
    "class_level_key: QTD_GreatSage",
    "runtime_copy_caster_state: false",
    "summon_count_stays_two_through_level_12: true",
    "no_extra_attack_on_clones: true",
    "do_not_require_bg3se_for_base_prototype: true",
)
for item in required_spec:
    if item not in spec:
        errors.append(f"Missing hair-clone spec: {item}")

for tier in TIERS:
    for item in (
        f"levels: {tier['levels']}",
        f"root_template_uuid: {tier['root']}",
        f"character_stats: {tier['character']}",
    ):
        if item not in spec:
            errors.append(f"Missing scaling tier field: {item}")

if 'new entry "Target_QTD_HairClones"' not in spells:
    errors.append("Missing Target_QTD_HairClones SpellData")
if 'data "UseCosts" "BonusActionPoint:1;QTD_SageQi:3"' not in spells:
    errors.append("Hair clone cost must remain Bonus Action + 3 Sage Qi")
if 'data "TargetConditions" "CanStand(\'8c17bf83-fc1d-4143-b555-46b38003bb49\')"' not in spells:
    errors.append("Hair clone spell must use the shared L6-footprint CanStand probe")

if spells.count("GROUND:IF(") != 8:
    errors.append("Level-scaling draft must contain 8 conditional ground summons (4 tiers x 2 clones)")
if spells.count(":Summon(") != 8:
    errors.append("Level-scaling draft must contain exactly 8 Summon functors")
if spells.count(",3,,false,") != 8:
    errors.append("Every tier summon must keep the 3-round lifetime")
if spells.count("QTD_STATUS_HAIR_CLONE,,,,false,true") != 8:
    errors.append("Every tier summon must apply clone status and enable bUseCasterPassives")

for stack_id in ("QTD_HairClone_A", "QTD_HairClone_B"):
    if spells.count(f"'{stack_id}'") != 4:
        errors.append(f"{stack_id} must be used once in each of four scaling tiers")

for tier in TIERS:
    prefix = f"GROUND:IF({tier['condition']}):Summon({tier['root']},3,,false,"
    if spells.count(prefix) != 2:
        errors.append(f"Scaling tier {tier['levels']} must execute both clone summons")

for tier in TIERS:
    expected = 3 if tier["root"] == "8c17bf83-fc1d-4143-b555-46b38003bb49" else 2
    if spells.count(tier["root"]) != expected:
        errors.append(f"Root {tier['root']} should appear {expected} times in HairClones.txt")

if 'new entry "QTD_STATUS_HAIR_CLONE"' not in statuses:
    errors.append("Missing QTD_STATUS_HAIR_CLONE")
if 'data "StatusType" "BOOST"' not in statuses:
    errors.append("Hair clone identification status must remain a BOOST draft")

for tier in TIERS:
    if f'new entry "{tier["character"]}"' not in characters:
        errors.append(f"Missing clone Character tier: {tier['character']}")
    for required_char in (
        f'data "Level" "{tier["level"]}"',
        f'data "Armor" "{tier["ac"]}"',
        f'data "Vitality" "{tier["hp"]}"',
    ):
        if required_char not in characters:
            errors.append(f"Missing clone scaling field: {required_char}")

for line in characters.splitlines():
    if line.startswith('data "Passives"') and "ExtraAttack" in line:
        errors.append("Clone scaling track must not grant Extra Attack")

for forbidden in (
    "runtime_copy_caster_state: true",
    "summon_count_stays_two_through_level_12: false",
    "no_extra_attack_on_clones: false",
):
    if forbidden in spec:
        errors.append(f"Forbidden scaling policy: {forbidden}")

rows = list(csv.DictReader(io.StringIO(spell_lists_text)))
l6 = next((row for row in rows if row["Name"] == "QTD_SpellList_L6"), None)
if not l6 or "Target_QTD_HairClones" not in l6["Spells"]:
    errors.append("Level 6 spell list must grant Target_QTD_HairClones")

if errors:
    print("HAIR CLONE SPEC VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("HAIR CLONE SPEC VALIDATION OK")
print("Validated L6/L8/L10/L12 fixed-template scaling, 2 clone slots, 3-round lifetime and no runtime caster copy.")
print("Runtime readiness: LEVEL-SCALING-DRAFT; local RootTemplate and class-token verification still required.")
