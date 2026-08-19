#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTS = {".md", ".txt", ".csv", ".yaml", ".yml", ".tsv", ".json", ".py"}
OLD = "Shout_" + "QTD_SomersaultCloud"
NEW = "Target_QTD_SomersaultCloud"
errors = []

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in TEXT_EXTS:
        continue
    if any(part in {".git", "__pycache__"} for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    if OLD in text:
        errors.append(f"stale Somersault Cloud TechName in {path.relative_to(ROOT)}")

required = {
    ROOT / "src/stats/Spells.txt",
    ROOT / "data/spells.yaml",
    ROOT / "data/spell_lists.csv",
    ROOT / "data/implementation_status.csv",
}
for path in required:
    if NEW not in path.read_text(encoding="utf-8"):
        errors.append(f"missing canonical {NEW} in {path.relative_to(ROOT)}")

if errors:
    print("CONSISTENCY CHECK FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("CONSISTENCY CHECK OK")
print(f"Canonical Somersault Cloud TechName: {NEW}")
