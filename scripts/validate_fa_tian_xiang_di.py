#!/usr/bin/env python3
from pathlib import Path
import csv
import io
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
passives = (ROOT / "src" / "stats" / "Passives.txt").read_text(encoding="utf-8")
stats = (ROOT / "src" / "stats" / "FaTianXiangDi.txt").read_text(encoding="utf-8")
hair_spells = (ROOT / "src" / "stats" / "HairClones.txt").read_text(encoding="utf-8")
hair_statuses = (ROOT / "src" / "stats" / "HairCloneStatuses.txt").read_text(encoding="utf-8")
three_heads = (ROOT / "src" / "stats" / "ThreeHeadsSixArms.txt").read_text(encoding="utf-8")
transforms = (ROOT / "src" / "stats" / "Transforms.txt").read_text(encoding="utf-8")
spec = (ROOT / "data" / "fa_tian_xiang_di.yaml").read_text(encoding="utf-8")
progressions_text = (ROOT / "data" / "progressions.csv").read_text(encoding="utf-8")
localization = (ROOT / "src" / "stats" / "Localization.tsv").read_text(encoding="utf-8")
implementation = (ROOT / "data" / "implementation_status.csv").read_text(encoding="utf-8")
manifest = json.loads((ROOT / "data" / "uuid_manifest.json").read_text(encoding="utf-8"))

errors = []

for item in (
    'new entry "QTD_Passive_FaTianXiangDi"',
    'UnlockSpell(Shout_QTD_FaTianXiangDi)',
):
    if item not in passives:
        errors.append(f"Missing Fa Tian passive field: {item}")

required_stats = (
    'new entry "Shout_QTD_FaTianXiangDi"',
    'data "UseCosts" "ActionPoint:1;QTD_SageQi:5"',
    'ApplyStatus(QTD_STATUS_FATIAN_XIANG_DI,100,3)',
    'ApplyStatus(QTD_STATUS_FATIAN_USED,100,-1)',
    "not HasStatus('SG_Polymorph')",
    "not HasStatus('SG_Invisible')",
    "not HasStatus('QTD_STATUS_HAIR_CLONES_ACTIVE')",
    "not HasStatus('QTD_STATUS_THREE_HEADS_SIX_ARMS')",
    "not HasStatus('QTD_STATUS_FATIAN_USED')",
    'new entry "QTD_STATUS_FATIAN_XIANG_DI"',
    'ObjectSize(+1)',
    'ScaleMultiplier(1.33)',
    'AbilityOverrideMinimum(Strength,25)',
    'Advantage(Ability,Strength)',
    'Advantage(SavingThrow,Strength)',
    'CharacterWeaponDamage(2d8,Force)',
    'CharacterWeaponDamage(2d8,Thunder)',
    'CarryCapacityMultiplier(2)',
    'StatusImmunity(SG_Frightened)',
    'UnlockSpell(Zone_QTD_FaTian_Quake)',
    'UnlockSpell(Zone_QTD_FaTian_Sweep)',
    'UnlockSpell(Target_QTD_FaTian_Pillar)',
    'new entry "QTD_STATUS_FATIAN_USED"',
    'RemoveOnLongRest',
    'new entry "Zone_QTD_FaTian_Quake"',
    'using "Zone_Thunderwave"',
    'not SavingThrow(Ability.Strength, SourceSpellDC())',
    'DealDamage(4d8,Thunder,Magical)',
    'ApplyStatus(PRONE,100,1)',
    'Force(3,OriginToEntity,Aggressive,true)',
    'new entry "Zone_QTD_FaTian_Sweep"',
    'using "Zone_Cleave"',
    'DealDamage(MainMeleeWeapon, MainMeleeWeaponDamageType)',
    'GROUND:ExecuteWeaponFunctors(MainHand)',
    'new entry "Target_QTD_FaTian_Pillar"',
    'using "Target_MainHandAttack"',
    'data "TargetRadius" "9"',
    'Force(6,OriginToEntity,Aggressive,true)',
)
for item in required_stats:
    if item not in stats:
        errors.append(f"Missing Fa Tian Stats field: {item}")

if stats.count('data "Cooldown" "OncePerTurn"') != 3:
    errors.append("Each of the three Fa Tian actions must have OncePerTurn cooldown")
if stats.count('data "RequirementConditions" "HasStatus(\'QTD_STATUS_FATIAN_XIANG_DI\')"') != 3:
    errors.append("All three Fa Tian actions must require the active form status")

executable_stats = "\n".join(line for line in stats.splitlines() if not line.lstrip().startswith("//"))
for forbidden in (
    'ObjectSize(+2)',
    'ExtraAttack_2',
    'ExtraAttack_3',
    'ActionResource(ActionPoint',
    'ActionPoint:2',
):
    if forbidden in executable_stats:
        errors.append(f"Forbidden/unsupported Fa Tian executable pattern: {forbidden}")

for item in (
    "unlock_level: 11",
    "sage_qi_cost: 5",
    "duration_rounds: 3",
    "once_per_long_rest: true",
    "object_size_delta: 1",
    "scale_multiplier: 1.33",
    "strength_floor: 25",
    "force_damage: 2d8",
    "thunder_damage: 2d8",
    "do_not_grant_extra_action_point: true",
    "do_not_grant_extra_attack_2: true",
    "do_not_claim_true_huge_collision_before_toolkit_test: true",
    "no_script_extender_required: true",
):
    if item not in spec:
        errors.append(f"Missing Fa Tian spec field: {item}")

rows = list(csv.DictReader(io.StringIO(progressions_text)))
l11 = next((row for row in rows if row["Name"] == "QTD_GreatSage_11"), None)
if not l11 or "QTD_Passive_FaTianXiangDi" not in l11["PassivesAdded"]:
    errors.append("Level 11 progression must grant QTD_Passive_FaTianXiangDi")

if 'new entry "QTD_STATUS_HAIR_CLONES_ACTIVE"' not in hair_statuses:
    errors.append("Hair clone system must define QTD_STATUS_HAIR_CLONES_ACTIVE")
if 'ApplyStatus(SELF,QTD_STATUS_HAIR_CLONES_ACTIVE,100,3)' not in hair_spells:
    errors.append("Hair clone cast must mark the caster active for 3 rounds")
if 'not HasStatus(\'QTD_STATUS_FATIAN_XIANG_DI\')' not in hair_spells:
    errors.append("Hair clones must be blocked during Fa Tian Xiang Di")
if 'not HasStatus(\'QTD_STATUS_FATIAN_XIANG_DI\')' not in three_heads:
    errors.append("Three Heads Six Arms must be blocked during Fa Tian Xiang Di")
if transforms.count("not HasStatus('QTD_STATUS_FATIAN_XIANG_DI')") != 3:
    errors.append("All three QTD transformation children must be blocked during Fa Tian Xiang Di")

for key in (
    "QTD_Passive_FaTianXiangDi_DisplayName",
    "Shout_QTD_FaTianXiangDi_DisplayName",
    "QTD_STATUS_FATIAN_XIANG_DI_DisplayName",
    "Zone_QTD_FaTian_Quake_DisplayName",
    "Zone_QTD_FaTian_Sweep_DisplayName",
    "Target_QTD_FaTian_Pillar_DisplayName",
):
    if key not in localization:
        errors.append(f"Missing Fa Tian localization key: {key}")

for status_line in (
    "Feature,QTD_FaTianXiangDi,V0.4,active-giant-form-draft",
    "Passive,QTD_Passive_FaTianXiangDi,V0.4,unlock-passive-draft",
    "Spell,Shout_QTD_FaTianXiangDi,V0.4,active-form-spell-draft",
    "Status,QTD_STATUS_FATIAN_XIANG_DI,V0.4,enlarge-aligned-giant-status-draft",
    "Status,QTD_STATUS_FATIAN_USED,V0.4,long-rest-marker-draft",
):
    if status_line not in implementation:
        errors.append(f"Missing Fa Tian implementation status: {status_line}")

for manifest_key in (
    "passive_fa_tian_uuid",
    "spell_fa_tian_uuid",
    "status_fa_tian_uuid",
    "status_fa_tian_used_uuid",
    "fa_tian_quake_uuid",
    "fa_tian_sweep_uuid",
    "fa_tian_pillar_uuid",
    "status_hair_clones_active_uuid",
):
    if manifest_key not in manifest["uuids"]:
        errors.append(f"Missing planning UUID: {manifest_key}")

if errors:
    print("FA TIAN XIANG DI VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("FA TIAN XIANG DI VALIDATION OK")
print("Validated L11 unlock, 5 Sage Qi giant form, 3-round duration, long-rest marker, STR floor 25, weapon empowerment, three form actions and mutual exclusion gates.")
print("Runtime readiness: ACTIVE-GIANT-FORM-DRAFT; true Huge collision, Pillar 9m melee targeting, animation/VFX and damage stacking still require local Patch 8 Toolkit testing.")
