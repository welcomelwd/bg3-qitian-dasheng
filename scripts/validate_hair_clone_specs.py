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

ROOT_TEMPLATE = "8c17bf83-fc1d-4143-b555-46b38003bb49"
errors = []

required_spec = (
    "spell: Target_QTD_HairClones",
    "unlock_level: 6",
    "sage_qi_cost: 3",
    "summon_count: 2",
    "lifetime_rounds: 3",
    "use_caster_passives: true",
    f"root_template_uuid: {ROOT_TEMPLATE}",
    "recast_replaces_existing_pair: true",
    "do_not_require_bg3se_for_base_prototype: true",
)
for item in required_spec:
    if item not in spec:
        errors.append(f"Missing hair-clone spec: {item}")

if 'new entry "Target_QTD_HairClones"' not in spells:
    errors.append("Missing Target_QTD_HairClones SpellData")
if 'data "UseCosts" "BonusActionPoint:1;QTD_SageQi:3"' not in spells:
    errors.append("Hair clone cost must be Bonus Action + 3 Sage Qi")
if f'data "TargetConditions" "CanStand(\'{ROOT_TEMPLATE}\')"' not in spells:
    errors.append("Hair clone spell must validate ground space with CanStand(root template)")
if spells.count("GROUND:Summon(") != 2:
    errors.append("Hair clone prototype must contain exactly two ground Summon functors")
for stack_id in ("QTD_HairClone_A", "QTD_HairClone_B"):
    if stack_id not in spells:
        errors.append(f"Missing summon StackID: {stack_id}")
if spells.count(",3,,false,") != 2:
    errors.append("Both summons must use a 3-round lifetime and no extended concentration")
if spells.count("QTD_STATUS_HAIR_CLONE,,,,false,true") != 2:
    errors.append("Both summons must apply clone status and enable bUseCasterPassives")

if 'new entry "QTD_STATUS_HAIR_CLONE"' not in statuses:
    errors.append("Missing QTD_STATUS_HAIR_CLONE")
if 'data "StatusType" "BOOST"' not in statuses:
    errors.append("Hair clone identification status must remain a BOOST draft")

if 'new entry "QTD_HairCloneCharacter_L6"' not in characters:
    errors.append("Missing fixed-stat L6 clone Character")
for required_char in (
    'using "Human_Commoner"',
    'data "Level" "6"',
    'data "Armor" "14"',
    'data "Vitality" "24"',
    'data "ActionResources" "ActionPoint:1;BonusActionPoint:1;Movement:9;ReactionActionPoint:1"',
):
    if required_char not in characters:
        errors.append(f"Missing clone Character field: {required_char}")
if "ExtraAttack" in characters:
    errors.append("L6 clone prototype must not have Extra Attack")

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
print("Validated L6 grant, 2 summons, 3-round lifetime, unique StackIDs, fixed clone stats and caster-passive bridge.")
print("Runtime readiness: SUMMON-FUNCTOR-DRAFT; local RootTemplate and collision verification still required.")
