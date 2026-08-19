#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
STATS = ROOT / "src" / "stats"
EXPECTED = {
    "QTD_Passive_MonkeyAgility",
    "QTD_Passive_RuyiMastery",
    "QTD_Passive_CopperHeadIronArm",
    "QTD_STATUS_CLOUD_MOMENTUM",
    "QTD_STATUS_DEMON_REVEALED",
    "Target_QTD_SomersaultCloud",
    "Target_QTD_FieryGoldenEyes",
    "Zone_QTD_SeaCalmingStrike",
    "WPN_QTD_RuyiJinguBang",
    "Target_QTD_RuyiExtend",
    "ARM_QTD_GoldenArmor",
    "BOOTS_QTD_CloudWalking",
}

found = set()
for path in STATS.glob("*.txt"):
    text = path.read_text(encoding="utf-8")
    found.update(re.findall(r'^new entry "([^"]+)"', text, re.M))

missing = EXPECTED - found
if missing:
    print("Missing draft entries:", ", ".join(sorted(missing)))
    sys.exit(1)

spells = (STATS / "Spells.txt").read_text(encoding="utf-8")
if 'using "Target_MistyStep"' not in spells:
    print("Somersault Cloud must retain Target_MistyStep as its verified parent reference")
    sys.exit(1)
if 'TeleportSource()' not in spells:
    print("Somersault Cloud must retain the documented TeleportSource() functor")
    sys.exit(1)
if 'SavingThrow(Ability.Strength, SourceSpellDC())' not in spells:
    print("Sea-Calming Strike must retain the documented Strength saving throw pattern")
    sys.exit(1)
if 'Force(3,OriginToEntity,Aggressive,true)' not in spells:
    print("Sea-Calming Strike must retain its documented 3m Force functor draft")
    sys.exit(1)

combined = "\n".join(p.read_text(encoding="utf-8") for p in STATS.glob("*.txt"))
for marker in (
    "TODO_TOOLKIT_CLONE_QUARTERSTAFF_TEMPLATE",
    "TODO_TOOLKIT_CLONE_ARMOR_PARENT",
    "TODO_TOOLKIT_CLONE_BOOTS_PARENT",
):
    if marker not in combined:
        print(f"Expected safe placeholder missing: {marker}")
        sys.exit(1)

print(f"STATS DRAFT VALIDATION OK: {len(found)} entries found")
print("Verified patterns: Target_MistyStep, TeleportSource, Strength save, Force")
print("Runtime readiness: NO (Toolkit clone gates remain by design)")
