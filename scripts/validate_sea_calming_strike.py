#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SPELLS = (ROOT / "src" / "stats" / "Spells.txt").read_text(encoding="utf-8")
SPECS = (ROOT / "data" / "spells.yaml").read_text(encoding="utf-8")
DOC = (ROOT / "docs" / "V01_SEA_CALMING_STRIKE.md").read_text(encoding="utf-8")

required_spell_markers = [
    'new entry "Zone_QTD_SeaCalmingStrike"',
    'using "Zone_Cleave"',
    'data "SpellRoll" "not SavingThrow(Ability.Strength, SourceSpellDC())"',
    'DealDamage(MainMeleeWeapon,MainWeaponDamageType)',
    'GROUND:ExecuteWeaponFunctors(MainHand)',
    "not ClassLevelHigherOrEqualThan(5,'QTD_GreatSage')",
    "ClassLevelHigherOrEqualThan(5,'QTD_GreatSage') and not ClassLevelHigherOrEqualThan(11,'QTD_GreatSage')",
    "ClassLevelHigherOrEqualThan(11,'QTD_GreatSage')",
    'DealDamage(2d8,Thunder,Magical)',
    'DealDamage(3d8,Thunder,Magical)',
    'DealDamage(4d8,Thunder,Magical)',
    'DealDamage(2d8/2,Thunder,Magical)',
    'DealDamage(3d8/2,Thunder,Magical)',
    'DealDamage(4d8/2,Thunder,Magical)',
    'ApplyStatus(PRONE,100,1)',
    'Force(3,OriginToEntity,Aggressive,true)',
    'data "Shape" "Cone"',
    'data "Range" "3"',
    'data "Angle" "120"',
    'data "UseCosts" "ActionPoint:1;QTD_SageQi:2"',
]

missing = [marker for marker in required_spell_markers if marker not in SPELLS]
if missing:
    print("SEA-CALMING STRIKE VALIDATION FAILED")
    for marker in missing:
        print("missing:", marker)
    sys.exit(1)

for marker in (
    "runtime_state: weapon-zone-scaling-draft",
    "level_3: 2d8",
    "level_5: 3d8",
    "level_11: 4d8",
    "successful_save: half thunder damage",
):
    if marker not in SPECS:
        print("SEA-CALMING STRIKE SPEC FAILED: missing", marker)
        sys.exit(1)

for marker in (
    "L3、L4 的额外雷鸣必须为 2d8",
    "L5-L10 必须为 3d8",
    "L11-L12 必须为 4d8",
    "不要标记 `toolkit-verified`",
):
    if marker not in DOC:
        print("SEA-CALMING STRIKE DOC FAILED: missing", marker)
        sys.exit(1)

# Guard against regressing to the old thunder-only draft.
entry = SPELLS.split('new entry "Zone_QTD_SeaCalmingStrike"', 1)[1]
if 'DealDamage(MainMeleeWeapon,MainWeaponDamageType)' not in entry:
    print("SEA-CALMING STRIKE VALIDATION FAILED: weapon component missing")
    sys.exit(1)

print("SEA-CALMING STRIKE VALIDATION OK")
print("Runtime state: weapon-zone-scaling-draft; owner Toolkit/game validation pending.")
