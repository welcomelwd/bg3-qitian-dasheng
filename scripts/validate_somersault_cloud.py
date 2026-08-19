#!/usr/bin/env python3
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
STATS = ROOT / "src" / "stats"

spells = (STATS / "Spells.txt").read_text(encoding="utf-8")
statuses = (STATS / "Statuses.txt").read_text(encoding="utf-8")
passives = (STATS / "Passives.txt").read_text(encoding="utf-8")
localization = (STATS / "Localization.tsv").read_text(encoding="utf-8")
spells_spec = (ROOT / "data" / "spells.yaml").read_text(encoding="utf-8")
implementation = (ROOT / "data" / "implementation_status.csv").read_text(encoding="utf-8")
runtime_matrix = (ROOT / "data" / "runtime_validation_matrix.csv").read_text(encoding="utf-8")


def require(text: str, needle: str, message: str) -> None:
    if needle not in text:
        print(message)
        sys.exit(1)


# Base spell contract.
for needle, message in (
    ('new entry "Target_QTD_SomersaultCloud"', "Somersault Cloud spell entry missing"),
    ('using "Target_MistyStep"', "Somersault Cloud must retain Target_MistyStep parent"),
    ('data "TargetRadius" "12"', "Somersault Cloud base range must remain 12m"),
    ('data "UseCosts" "BonusActionPoint:1;QTD_SageQi:1"', "Somersault Cloud must cost Bonus Action + 1 Sage Qi"),
    ('data "SpellProperties" "TeleportSource();ApplyStatus(SELF,QTD_STATUS_CLOUD_MOMENTUM,100,1)"', "Somersault Cloud must teleport then apply 1-turn Cloud Momentum to SELF"),
):
    require(spells, needle, message)

# Cloud Momentum contract.
for needle, message in (
    ('new entry "QTD_STATUS_CLOUD_MOMENTUM"', "Cloud Momentum status missing"),
    ('IF(IsMeleeAttack()):Advantage(AttackRoll)', "Cloud Momentum must only grant melee AttackRoll Advantage"),
    ('data "Passives" "QTD_Passive_CloudMomentum_Consume"', "Cloud Momentum must attach its consume helper"),
):
    require(statuses, needle, message)

for needle, message in (
    ('new entry "QTD_Passive_CloudMomentum_Consume"', "Cloud Momentum consume passive missing"),
    ('data "StatsFunctorContext" "OnAttack"', "Cloud Momentum consume helper must use OnAttack"),
    ('data "Conditions" "IsMeleeAttack()"', "Cloud Momentum consume helper must only consume on melee attacks"),
    ('data "StatsFunctors" "RemoveStatus(SELF,QTD_STATUS_CLOUD_MOMENTUM)"', "Cloud Momentum consume helper must remove the status"),
):
    require(passives, needle, message)

# Cumulative range modifiers: 12 -> 15 -> 18 -> ~21.
range_passives = {
    "QTD_Passive_SomersaultCloud_Range_L5": "ModifyTargetRadius(Multiplicative,1.25)",
    "QTD_Passive_SomersaultCloud_Range_L9": "ModifyTargetRadius(Multiplicative,1.2)",
    "QTD_Passive_SomersaultCloud_Range_L12": "ModifyTargetRadius(Multiplicative,1.1666667)",
}
for tech_name, modifier in range_passives.items():
    require(passives, f'new entry "{tech_name}"', f"Missing range passive {tech_name}")
    require(passives, modifier, f"Incorrect target-radius modifier for {tech_name}")
    require(passives, "SpellId('Target_QTD_SomersaultCloud')", "Range passives must target the existing Somersault Cloud spell")

with (ROOT / "data" / "progressions.csv").open(encoding="utf-8", newline="") as fh:
    rows = list(csv.DictReader(fh))
main_rows = {int(r["Level"]): r for r in rows if r["ProgressionType"] == "0" and r["Name"].startswith("QTD_GreatSage_")}
for level, tech_name in ((5, "QTD_Passive_SomersaultCloud_Range_L5"), (9, "QTD_Passive_SomersaultCloud_Range_L9"), (12, "QTD_Passive_SomersaultCloud_Range_L12")):
    if level not in main_rows or tech_name not in main_rows[level]["PassivesAdded"].split(";"):
        print(f"Level {level} must grant {tech_name}")
        sys.exit(1)

for needle, message in (
    ("2: 12", "spells.yaml must record L2 = 12m"),
    ("5: 15", "spells.yaml must record L5 = 15m"),
    ("9: 18", "spells.yaml must record L9 = 18m"),
    ("12: 21", "spells.yaml must record L12 = 21m"),
    ("ranged_attacks_do_not_consume: true", "spells.yaml must preserve ranged non-consumption"),
):
    require(spells_spec, needle, message)

require(localization, "首次近战攻击后云势消散", "Localization must describe first-melee consumption")
require(implementation, "Spell,Target_QTD_SomersaultCloud,V0.1,momentum-range-scaling-draft", "Implementation status must advance Somersault Cloud")
require(implementation, "Status,QTD_STATUS_CLOUD_MOMENTUM,V0.1,next-melee-advantage-draft", "Implementation status must include Cloud Momentum")
require(runtime_matrix, "INT-006,P0,V0.1,Spell,Target_QTD_SomersaultCloud,2,Base,BonusAction,1,momentum-range-scaling-draft", "INT-006 runtime state is stale")

print("SOMERSAULT CLOUD VALIDATION OK")
print("Validated: Bonus Action + 1 Qi, SELF Cloud Momentum, melee-only Advantage consumption, 12/15/18/21m progression wiring.")
print("Runtime readiness: PATTERN-ALIGNED-DRAFT; Patch 8 Toolkit timing and stacked radius verification still required.")
