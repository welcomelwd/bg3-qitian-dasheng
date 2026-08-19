#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []


def read_csv(rel):
    with (ROOT / rel).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


progressions = read_csv("data/progressions.csv")
class_desc = read_csv("data/class_descriptions.csv")
resources = read_csv("data/action_resources.csv")
spell_lists = read_csv("data/spell_lists.csv")
recording = read_csv("data/toolkit_spine_recording.csv")
manifest = json.loads((ROOT / "data/uuid_manifest.json").read_text(encoding="utf-8"))["uuids"]
passives = (ROOT / "src/stats/Passives.txt").read_text(encoding="utf-8")
implementation_doc = (ROOT / "docs/TOOLKIT_IMPLEMENTATION.md").read_text(encoding="utf-8")
spine_doc = (ROOT / "docs/V01_CLASS_RESOURCE_SPINE.md").read_text(encoding="utf-8")
workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

main = [r for r in progressions if r.get("Name", "").startswith("QTD_GreatSage_") and r.get("ProgressionType") == "0"]
if len(main) != 12:
    errors.append(f"Expected 12 main-class progression rows, found {len(main)}")
else:
    levels = sorted(int(r["Level"]) for r in main)
    if levels != list(range(1, 13)):
        errors.append(f"Main progression levels must be 1..12, got {levels}")

    table_uuids = {r["TableUUID"] for r in main}
    if table_uuids != {manifest["class_table_uuid"]}:
        errors.append(f"Main progression TableUUID mismatch: {sorted(table_uuids)}")

    row_uuids = [r["UUID"] for r in main]
    if len(row_uuids) != len(set(row_uuids)):
        errors.append("Main progression row UUIDs must be unique")

    feats = {int(r["Level"]) for r in main if r.get("AllowImprovement") == "Yes"}
    if feats != {4, 8, 12}:
        errors.append(f"AllowImprovement must be Yes only at 4/8/12, got {sorted(feats)}")

by_level = {int(r["Level"]): r for r in main}
if 5 in by_level and "QTD_Passive_ExtraAttack" not in (by_level[5].get("PassivesAdded") or ""):
    errors.append("L5 must grant QTD_Passive_ExtraAttack")

expected_selectors = {
    2: f"AddSpells({manifest['spelllist_l2_uuid']})",
    3: f"AddSpells({manifest['spelllist_l3_uuid']})",
    6: f"AddSpells({manifest['spelllist_l6_uuid']})",
}
for level, selector in expected_selectors.items():
    row = by_level.get(level)
    if not row or selector not in (row.get("Selectors") or ""):
        errors.append(f"L{level} must include selector {selector}")

expected_subclasses = {
    "QTD_VictoriousBuddha",
    "QTD_SeventyTwoChanges",
    "QTD_SpiritualStoneMonkey",
}
if 3 in by_level:
    actual = {x for x in (by_level[3].get("SubClasses") or "").split(";") if x}
    if actual != expected_subclasses:
        errors.append(f"L3 subclasses mismatch: {sorted(actual)}")

expected_qi_increments = {1: 2, 2: 1, 5: 1, 8: 1, 11: 1}
actual_qi_increments = {}
for row in main:
    level = int(row["Level"])
    amounts = [int(x) for x in re.findall(r"ActionResource\(QTD_SageQi,(\d+),0\)", row.get("Boosts") or "")]
    if amounts:
        actual_qi_increments[level] = sum(amounts)
if actual_qi_increments != expected_qi_increments:
    errors.append(f"Sage Qi increments mismatch: {actual_qi_increments}, expected {expected_qi_increments}")
if sum(actual_qi_increments.values()) != 6:
    errors.append("Base L1-L11 Sage Qi capacity must total 6")
if "ActionResource(QTD_SageQi,2,0)" not in passives:
    errors.append("L12 Qitian Dasheng passive must retain Sage Qi +2")

sage_qi = next((r for r in resources if r.get("Name") == "QTD_SageQi"), None)
if not sage_qi:
    errors.append("QTD_SageQi missing from action_resources.csv")
else:
    if sage_qi.get("UUID") != manifest["resource_sage_qi_uuid"]:
        errors.append("QTD_SageQi planned UUID mismatch between action_resources.csv and manifest")
    if sage_qi.get("Recovery") != "ShortRest":
        errors.append("QTD_SageQi Recovery must remain ShortRest")
    if sage_qi.get("ShowOnActionResourcePanel") != "Yes":
        errors.append("QTD_SageQi must remain visible on Action Resource panel")

primary = next((r for r in class_desc if r.get("Name") == "QTD_GreatSage" and r.get("IsMulticlass") == "No"), None)
multiclass = next((r for r in class_desc if r.get("Name") == "QTD_GreatSage" and r.get("IsMulticlass") == "Yes"), None)
for label, row in (("primary", primary), ("multiclass", multiclass)):
    if not row:
        errors.append(f"Missing {label} QTD_GreatSage ClassDescriptions row")
        continue
    if row.get("ProgressionTableUUID") != manifest["class_table_uuid"]:
        errors.append(f"{label} ClassDescriptions ProgressionTableUUID mismatch")
    if row.get("PrimaryAbility") != "Strength" or row.get("SpellCastingAbility") != "Wisdom":
        errors.append(f"{label} ClassDescriptions must be Strength/Wisdom")
    if row.get("BaseHp") != "10" or row.get("HPPerLevel") != "6":
        errors.append(f"{label} ClassDescriptions HP must be 10 + 6/level")
    if (row.get("CommonHotbarColumns"), row.get("ClassHotbarColumns"), row.get("ItemsHotbarColumns")) != ("9", "5", "2"):
        errors.append(f"{label} ClassDescriptions hotbar columns must be 9/5/2")
if primary and multiclass and primary.get("UUID") == multiclass.get("UUID"):
    errors.append("Primary and multiclass ClassDescriptions UUIDs must differ")
if primary and primary.get("UUID") != manifest["class_primary_uuid"]:
    errors.append("Primary ClassDescriptions UUID mismatch with manifest")
if multiclass and multiclass.get("UUID") != manifest["class_multiclass_uuid"]:
    errors.append("Multiclass ClassDescriptions UUID mismatch with manifest")

spell_by_name = {r["Name"]: r for r in spell_lists}
expected_spell_lists = {
    "QTD_SpellList_L2": (manifest["spelllist_l2_uuid"], "Target_QTD_SomersaultCloud", "2"),
    "QTD_SpellList_L3": (manifest["spelllist_l3_uuid"], "Zone_QTD_SeaCalmingStrike", "3"),
    "QTD_SpellList_L6": (manifest["spelllist_l6_uuid"], "Target_QTD_FieryGoldenEyes;Target_QTD_HairClones", "6"),
}
for name, (uuid, spells, level) in expected_spell_lists.items():
    row = spell_by_name.get(name)
    if not row:
        errors.append(f"Missing {name}")
        continue
    if (row.get("UUID"), row.get("Spells"), row.get("GrantedAtLevel")) != (uuid, spells, level):
        errors.append(f"{name} definition mismatch")

expected_recording_names = {
    "QTD_GreatSage",
    "QTD_GreatSage_Multiclass",
    "QTD_SageQi",
    *(f"QTD_GreatSage_{level}" for level in range(1, 13)),
    "QTD_SpellList_L2",
    "QTD_SpellList_L3",
    "QTD_SpellList_L6",
}
recorded_names = {r.get("TechName") for r in recording}
missing_recording = expected_recording_names - recorded_names
if missing_recording:
    errors.append(f"Toolkit recording sheet missing: {sorted(missing_recording)}")

allowed_states = {
    "pending-toolkit-entry",
    "entered-not-tested",
    "basic-level-a-pass",
    "combat-pass",
    "toolkit-verified",
}
uuid_re = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")
for row in recording:
    state = row.get("LocalState") or ""
    toolkit_uuid = row.get("ToolkitUUID") or ""
    if state not in allowed_states:
        errors.append(f"Invalid LocalState for {row.get('TechName')}: {state}")
    if toolkit_uuid and not uuid_re.match(toolkit_uuid):
        errors.append(f"ToolkitUUID is not a UUID for {row.get('TechName')}: {toolkit_uuid}")
    if state == "toolkit-verified" and not toolkit_uuid:
        errors.append(f"toolkit-verified row must have ToolkitUUID: {row.get('TechName')}")

for stale in ("Shout_QTD_SomersaultCloud",):
    if stale in implementation_doc or stale in spine_doc:
        errors.append(f"Stale canonical TechName remains in Toolkit docs: {stale}")

for token in (
    "Target_QTD_SomersaultCloud",
    "Zone_QTD_SeaCalmingStrike",
    "Target_QTD_FieryGoldenEyes;Target_QTD_HairClones",
    "L1 = 2",
    "L12",
    "Multiclass",
):
    if token not in spine_doc:
        errors.append(f"Spine document missing required token: {token}")

if "python scripts/validate_class_resource_spine.py" not in workflow:
    errors.append("GitHub Actions must run validate_class_resource_spine.py")

if errors:
    print("CLASS / RESOURCE SPINE VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("CLASS / RESOURCE SPINE VALIDATION OK")
print("Validated 12-level progression, 4/8/12 feats, 3 subclasses, spell lists, and Sage Qi 2/3/4/5/6 -> 8 capstone curve.")
print("Runtime readiness: PENDING LOCAL PATCH 8 TOOLKIT ENTRY AND BASIC_LEVEL_A TESTS.")
