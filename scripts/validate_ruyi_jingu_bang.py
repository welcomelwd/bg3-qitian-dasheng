#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
WEAPONS = (ROOT / "src" / "stats" / "Weapons.txt").read_text(encoding="utf-8")
ITEMS = (ROOT / "data" / "items.yaml").read_text(encoding="utf-8")
STATUS = (ROOT / "data" / "implementation_status.csv").read_text(encoding="utf-8")
MATRIX = (ROOT / "data" / "runtime_validation_matrix.csv").read_text(encoding="utf-8")
RECORDING = (ROOT / "data" / "toolkit_item_recording.csv").read_text(encoding="utf-8")
DOC = (ROOT / "docs" / "V01_RUYI_JINGU_BANG.md").read_text(encoding="utf-8")

checks = {
    "weapon": [
        'new entry "WPN_QTD_RuyiJinguBang"',
        'using "WPN_Quarterstaff"',
        'data "RootTemplate" "521284c4-3d7b-4642-9c26-3677198f5a69"',
        'data "Damage" "1d8"',
        'data "VersatileDamage" "1d10"',
        'data "WeaponRange" "300"',
        'Reach;Magical',
        'WeaponEnchantment(2)',
        'WeaponDamage(1d4,Force)',
        'Ability(Strength,1)',
        'JumpMaxDistanceMultiplier(1.5)',
        'UnlockSpell(Target_QTD_RuyiExtend)',
    ],
    "extend": [
        'new entry "Target_QTD_RuyiExtend"',
        'using "Target_MainHandAttack"',
        'data "TargetRadius" "9"',
        'Attack(AttackType.MeleeWeaponAttack)',
        'DealDamage(MainMeleeWeapon, MainMeleeWeaponDamageType);ExecuteWeaponFunctors(MainHand)',
    ],
    "spec": [
        'runtime_state: quarterstaff-reach-root-draft',
        'parent_stats: WPN_Quarterstaff',
        'weapon_range_m: 3',
        'jump_distance_multiplier: 1.5',
        'behavior: main-hand melee weapon attack at extended range',
    ],
    "recording": [
        'QTD_RuyiJinguBang_Root,521284c4-3d7b-4642-9c26-3677198f5a69,96e2abaf-78ff-4dcb-a6a3-a5f0c348bd9f',
        'WeaponStats,WPN_QTD_RuyiJinguBang',
        'Spell,Target_QTD_RuyiExtend',
    ],
    "doc": [
        '96e2abaf-78ff-4dcb-a6a3-a5f0c348bd9f',
        'WeaponRange',
        'JumpMaxDistanceMultiplier(1.5)',
        '不要标记 `toolkit-verified`',
    ],
}

texts = {
    "weapon": WEAPONS,
    "extend": WEAPONS,
    "spec": ITEMS,
    "recording": RECORDING,
    "doc": DOC,
}

errors = []
for section, markers in checks.items():
    for marker in markers:
        if marker not in texts[section]:
            errors.append(f"{section}: missing {marker}")

for forbidden in [
    'TODO_TOOLKIT_CLONE_QUARTERSTAFF_TEMPLATE',
    'JumpMaxDistance(1.5)',
    'data "SpellProperties" "DealDamage(1d8,Force)"',
]:
    if forbidden in WEAPONS:
        errors.append(f"weapon: forbidden legacy marker {forbidden}")

if 'Item,WPN_QTD_RuyiJinguBang,V0.1,quarterstaff-root-draft' not in STATUS:
    errors.append("status: Ruyi Jingu Bang implementation status must be quarterstaff-root-draft")

if 'INT-009' not in MATRIX or 'quarterstaff-root-draft' not in MATRIX:
    errors.append("matrix: INT-009 must be quarterstaff-root-draft")

if errors:
    print("RUYI JINGU BANG VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("RUYI JINGU BANG VALIDATION OK")
print("Runtime state: quarterstaff-root-draft; owner Toolkit/game validation pending.")
