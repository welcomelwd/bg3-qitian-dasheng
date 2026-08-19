#!/usr/bin/env python3
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

passives = (ROOT / "src/stats/Passives.txt").read_text(encoding="utf-8")
copper = (ROOT / "src/stats/CopperHeadIronArm.txt").read_text(encoding="utf-8")
workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

with (ROOT / "data/progressions.csv").open(encoding="utf-8-sig", newline="") as f:
    progressions = list(csv.DictReader(f))
with (ROOT / "data/runtime_validation_matrix.csv").open(encoding="utf-8-sig", newline="") as f:
    matrix = list(csv.DictReader(f))
with (ROOT / "data/implementation_status.csv").open(encoding="utf-8-sig", newline="") as f:
    implementation = list(csv.DictReader(f))

for token in (
    'new entry "QTD_Passive_CopperHeadIronArm"',
    'data "TooltipUseCosts" "ReactionActionPoint:1"',
    'UnlockInterrupt(QTD_Interrupt_CopperHeadIronArm)',
):
    if token not in passives:
        errors.append(f"Passives.txt missing: {token}")

for token in (
    'new entry "QTD_Interrupt_CopperHeadIronArm"',
    'data "InterruptContext" "OnPreDamage"',
    'data "InterruptContextScope" "Self"',
    'data "Container" "YesNoDecision"',
    'IsAbleToReact(context.Observer)',
    'Self(context.Target,context.Observer)',
    'IsAttack()',
    'HasDamageEffectFlag(DamageFlags.Hit)',
    'SpellDamageTypeIs(DamageType.Bludgeoning)',
    'SpellDamageTypeIs(DamageType.Piercing)',
    'SpellDamageTypeIs(DamageType.Slashing)',
    'ApplyStatus(OBSERVER_TARGET,QTD_STATUS_COPPER_HEAD_IRON_ARM_REDUCTION,100,1)',
    'data "Cost" "ReactionActionPoint:1"',
    'data "InterruptDefaultValue" "Ask;Enabled"',
    'data "EnableCondition" "not HasStatus(\'SG_Polymorph\')"',
    'new entry "QTD_STATUS_COPPER_HEAD_IRON_ARM_REDUCTION"',
    'DamageReduction(Bludgeoning, Flat, 1d8+WisdomModifier)',
    'DamageReduction(Piercing, Flat, 1d8+WisdomModifier)',
    'DamageReduction(Slashing, Flat, 1d8+WisdomModifier)',
    'new entry "QTD_Passive_CopperHeadIronArm_Cleanup"',
    'data "StatsFunctorContext" "OnDamaged;OnDamagedPrevented"',
    'RemoveStatus(QTD_STATUS_COPPER_HEAD_IRON_ARM_REDUCTION)',
):
    if token not in copper:
        errors.append(f"CopperHeadIronArm.txt missing: {token}")

if 'DamageReduction(All' in copper:
    errors.append("Copper Head / Iron Arm must not reduce elemental or other non-B/P/S damage via DamageReduction(All,...)")

l2 = next((r for r in progressions if r.get("Name") == "QTD_GreatSage_2"), None)
if not l2 or "QTD_Passive_CopperHeadIronArm" not in (l2.get("PassivesAdded") or ""):
    errors.append("L2 progression must grant QTD_Passive_CopperHeadIronArm")

row = next((r for r in matrix if r.get("ID") == "INT-005"), None)
if not row:
    errors.append("runtime_validation_matrix.csv missing INT-005")
else:
    if row.get("RuntimeState") != "interrupt-pattern-aligned-draft":
        errors.append("INT-005 RuntimeState must be interrupt-pattern-aligned-draft")
    if row.get("ReleaseBlocking") != "yes":
        errors.append("INT-005 must remain release-blocking until local Toolkit validation")

impl = {(r.get("Type"), r.get("TechName")): r.get("Status") for r in implementation}
expected_impl = {
    ("Passive", "QTD_Passive_CopperHeadIronArm"): "interrupt-pattern-aligned-draft",
    ("Interrupt", "QTD_Interrupt_CopperHeadIronArm"): "onpredamage-reaction-draft",
    ("Status", "QTD_STATUS_COPPER_HEAD_IRON_ARM_REDUCTION"): "physical-flat-reduction-draft",
}
for key, expected in expected_impl.items():
    if impl.get(key) != expected:
        errors.append(f"implementation_status.csv mismatch for {key}: {impl.get(key)!r}")

if "python scripts/validate_copper_head_iron_arm.py" not in workflow:
    errors.append("GitHub Actions must run validate_copper_head_iron_arm.py")

if errors:
    print("COPPER HEAD / IRON ARM VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("COPPER HEAD / IRON ARM VALIDATION OK")
print("Validated L2 unlock, OnPreDamage reaction prompt, B/P/S-only 1d8+WIS reduction, and cleanup after damage resolution.")
print("Runtime readiness: INTERRUPT-PATTERN-ALIGNED-DRAFT; local Patch 8 Toolkit combat validation still required.")
