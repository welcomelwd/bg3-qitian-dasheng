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
    "Shout_QTD_SomersaultCloud",
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
print("Runtime readiness: NO (Toolkit clone gates remain by design)")
