#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SPELLS = (ROOT / "src" / "stats" / "Spells.txt").read_text(encoding="utf-8")
STATUSES = (ROOT / "src" / "stats" / "Statuses.txt").read_text(encoding="utf-8")
PASSIVES = (ROOT / "src" / "stats" / "Passives.txt").read_text(encoding="utf-8")
PROGRESSIONS = (ROOT / "data" / "progressions.csv").read_text(encoding="utf-8")
SPECS = (ROOT / "data" / "spells.yaml").read_text(encoding="utf-8")
DOC = (ROOT / "docs" / "V01_FIERY_GOLDEN_EYES.md").read_text(encoding="utf-8")

checks = {
    "spell": [
        'new entry "Target_QTD_FieryGoldenEyes"',
        'data "TargetRadius" "18"',
        'data "UseCosts" "BonusActionPoint:1;QTD_SageQi:1"',
        'ApplyStatus(QTD_STATUS_DEMON_REVEALED,100,3)',
    ],
    "status": [
        'new entry "QTD_STATUS_DEMON_REVEALED"',
        'data "StackId" "QTD_STATUS_DEMON_REVEALED"',
        'AC(-2);StatusImmunity(SG_Invisible)',
        'RemoveStatus(SG_Invisible)',
    ],
    "passive": [
        'new entry "QTD_Passive_FieryGoldenEyes_TargetAdvantage"',
        'data "Properties" "IsHidden"',
        "HasStatus('QTD_STATUS_DEMON_REVEALED',context.Target,context.Source)",
        'Advantage(AttackRoll)',
        'data "StatsFunctorContext" "OnAttack"',
    ],
    "progression": [
        'QTD_GreatSage_6',
        'QTD_Passive_FieryGoldenEyes_TargetAdvantage',
        'AddSpells(986ba61c-a6cf-4b9e-be8e-075148e5f853)',
    ],
    "spec": [
        'runtime_state: source-bound-reveal-draft',
        'on_apply: RemoveStatus(SG_Invisible)',
        'invisibility_immunity: StatusImmunity(SG_Invisible)',
        'ac_penalty: -2',
        'party_wide: false',
    ],
    "doc": [
        'QTD_Passive_FieryGoldenEyes_TargetAdvantage',
        "HasStatus('QTD_STATUS_DEMON_REVEALED',context.Target,context.Source)",
        '不要标记 `toolkit-verified`',
    ],
}

texts = {
    "spell": SPELLS,
    "status": STATUSES,
    "passive": PASSIVES,
    "progression": PROGRESSIONS,
    "spec": SPECS,
    "doc": DOC,
}

errors = []
for section, markers in checks.items():
    for marker in markers:
        if marker not in texts[section]:
            errors.append(f"{section}: missing {marker}")

# Scope guard: the target status itself must not grant party-wide Advantage(AttackTarget).
status_entry = STATUSES.split('new entry "QTD_STATUS_DEMON_REVEALED"', 1)[1]
if 'Advantage(AttackTarget)' in status_entry.split('new entry "', 1)[0]:
    errors.append("status: target-side Advantage(AttackTarget) would make Fiery Golden Eyes party-wide")

if errors:
    print("FIERY GOLDEN EYES VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("FIERY GOLDEN EYES VALIDATION OK")
print("Runtime state: source-bound-reveal-draft; owner Toolkit/game validation pending.")
