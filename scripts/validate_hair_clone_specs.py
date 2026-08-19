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
weapons = (ROOT / "src" / "stats" / "HairCloneWeapons.txt").read_text(encoding="utf-8")
spell_lists_text = (ROOT / "data" / "spell_lists.csv").read_text(encoding="utf-8")

TIERS = [
    {"levels": "6-7", "root": "8c17bf83-fc1d-4143-b555-46b38003bb49", "character": "QTD_HairCloneCharacter_L6", "level": "6", "hp": "24", "ac": "14", "condition": "not ClassLevelHigherOrEqualThan(8,'QTD_GreatSage')"},
    {"levels": "8-9", "root": "122996e7-46e1-4f04-b64d-30db7c9a47ac", "character": "QTD_HairCloneCharacter_L8", "level": "8", "hp": "32", "ac": "15", "condition": "ClassLevelHigherOrEqualThan(8,'QTD_GreatSage') and not ClassLevelHigherOrEqualThan(10,'QTD_GreatSage')"},
    {"levels": "10-11", "root": "72fdc168-2ec4-45ed-a230-21df703ff6c0", "character": "QTD_HairCloneCharacter_L10", "level": "10", "hp": "40", "ac": "16", "condition": "ClassLevelHigherOrEqualThan(10,'QTD_GreatSage') and not ClassLevelHigherOrEqualThan(12,'QTD_GreatSage')"},
    {"levels": "12", "root": "b3368e82-088a-46fb-b8ec-dbc5dc5d4fe0", "character": "QTD_HairCloneCharacter_L12", "level": "12", "hp": "48", "ac": "17", "condition": "ClassLevelHigherOrEqualThan(12,'QTD_GreatSage')"},
]
WEAPON_ROOT = "757f581b-683f-40ac-8051-47c10ef651a2"
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
    "weapon_stats: WPN_QTD_HairCloneStaff",
    f"weapon_root_template_uuid: {WEAPON_ROOT}",
    "shared_across_all_clone_tiers: true",
    "one_shared_scaling_clone_weapon: true",
    "clone_weapon_has_no_active_ruyi_skills: true",
    "summon_count_stays_two_through_level_12: true",
    "no_extra_attack_on_clones: true",
    "do_not_require_bg3se_for_base_prototype: true",
)
for item in required_spec:
    if item not in spec:
        errors.append(f"Missing hair-clone spec: {item}")

for tier in TIERS:
    for item in (f"levels: {tier['levels']}", f"root_template_uuid: {tier['root']}", f"character_stats: {tier['character']}"):
        if item not in spec:
            errors.append(f"Missing scaling tier field: {item}")

if 'new entry "Target_QTD_HairClones"' not in spells:
    errors.append("Missing Target_QTD_HairClones SpellData")
if 'data "UseCosts" "BonusActionPoint:1;QTD_SageQi:3"' not in spells:
    errors.append("Hair clone cost must remain Bonus Action + 3 Sage Qi")
if 'data "TargetConditions" "CanStand(\'8c17bf83-fc1d-4143-b555-46b38003bb49\')"' not in spells:
    errors.append("Hair clone spell must use the shared L6-footprint CanStand probe")
if spells.count("GROUND:IF(") != 8 or spells.count(":Summon(") != 8:
    errors.append("Level-scaling draft must contain exactly 8 conditional Summon functors")
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

if 'new entry "QTD_STATUS_HAIR_CLONE"' not in statuses or 'data "StatusType" "BOOST"' not in statuses:
    errors.append("Missing/invalid QTD_STATUS_HAIR_CLONE")
for tier in TIERS:
    if f'new entry "{tier["character"]}"' not in characters:
        errors.append(f"Missing clone Character tier: {tier['character']}")
    for required_char in (f'data "Level" "{tier["level"]}"', f'data "Armor" "{tier["ac"]}"', f'data "Vitality" "{tier["hp"]}"'):
        if required_char not in characters:
            errors.append(f"Missing clone scaling field: {required_char}")
for line in characters.splitlines():
    if line.startswith('data "Passives"') and "ExtraAttack" in line:
        errors.append("Clone scaling track must not grant Extra Attack")

weapon_required = (
    'new entry "WPN_QTD_HairCloneStaff"',
    'type "Weapon"',
    'using "WPN_Quarterstaff"',
    f'data "RootTemplate" "{WEAPON_ROOT}"',
    'data "PassivesOnEquip" ""',
    'data "Weapon Properties" "Melee;Dippable;Versatile;Magical"',
    'WeaponProperty(Magical)',
    'CharacterLevelGreaterThan(7)',
    'CharacterLevelGreaterThan(9)',
    'CharacterLevelGreaterThan(11)',
)
for item in weapon_required:
    if item not in weapons:
        errors.append(f"Missing clone weapon field/pattern: {item}")
if weapons.count("WeaponEnchantment(1)") != 2:
    errors.append("Clone weapon must use +1 enchantment in exactly two level branches")
if weapons.count("WeaponEnchantment(2)") != 1:
    errors.append("Clone weapon must use +2 enchantment only in the L12+ branch")
if weapons.count("WeaponDamage(1d4,Force)") != 2:
    errors.append("Clone weapon must add 1d4 Force in L10-11 and L12+ branches")
for forbidden in ("Target_QTD_RuyiExtend", "Ability(Strength,1)", "JumpMaxDistance"):
    if forbidden in weapons:
        errors.append(f"Clone weapon must not contain real Jingu Bang feature: {forbidden}")

for forbidden in ("runtime_copy_caster_state: true", "summon_count_stays_two_through_level_12: false", "no_extra_attack_on_clones: false"):
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
print("Validated fixed clone tiers plus one shared level-scaling clone staff.")
print("Runtime readiness: LEVEL-SCALING-WEAPON-DRAFT; local RootTemplate, equipment and class-token verification still required.")
