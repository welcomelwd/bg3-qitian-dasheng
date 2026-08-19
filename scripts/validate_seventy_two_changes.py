#!/usr/bin/env python3
from pathlib import Path
import csv, io, json, sys, uuid

ROOT = Path(__file__).resolve().parents[1]
errors = []

progressions = list(csv.DictReader(io.StringIO((ROOT / "data/progressions.csv").read_text(encoding="utf-8"))))
class_desc = list(csv.DictReader(io.StringIO((ROOT / "data/class_descriptions.csv").read_text(encoding="utf-8"))))
subclasses = (ROOT / "data/subclasses.yaml").read_text(encoding="utf-8")
spec = (ROOT / "data/seventy_two_changes.yaml").read_text(encoding="utf-8")
stats = (ROOT / "src/stats/SeventyTwoChangesSubclass.txt").read_text(encoding="utf-8")
loc = (ROOT / "src/stats/Localization_SeventyTwoChanges.tsv").read_text(encoding="utf-8")
impl = (ROOT / "data/implementation_status.csv").read_text(encoding="utf-8")
manifest = json.loads((ROOT / "data/uuid_manifest.json").read_text(encoding="utf-8"))

main_l3 = next((r for r in progressions if r["Name"] == "QTD_GreatSage_3"), None)
if not main_l3:
    errors.append("Missing QTD_GreatSage_3")
else:
    for subclass in ("QTD_VictoriousBuddha", "QTD_SeventyTwoChanges"):
        if subclass not in (main_l3["SubClasses"] or ""):
            errors.append(f"Main L3 must expose {subclass}")

sub = [r for r in progressions if r["Name"].startswith("QTD_SeventyTwoChanges_")]
if [int(r["Level"]) for r in sub] != [3, 6, 10]:
    errors.append("Seventy-Two Changes progression levels must be 3,6,10")
if any(r["ProgressionType"] != "1" for r in sub):
    errors.append("Seventy-Two Changes rows must use ProgressionType=1")
if len({r["TableUUID"] for r in sub}) != 1 or (sub and sub[0]["TableUUID"] != "4d2f7b28-c2a8-4bde-9df1-04e2e6c6c1b5"):
    errors.append("Seventy-Two Changes TableUUID mismatch")

expected_passives = {
    3: "QTD_Passive_SeventyTwoChanges_L3",
    6: "QTD_Passive_SeventyTwoChanges_L6",
    10: "QTD_Passive_SeventyTwoChanges_L10",
}
for r in sub:
    level = int(r["Level"])
    if expected_passives.get(level) not in (r["PassivesAdded"] or ""):
        errors.append(f"L{level} missing expected Seventy-Two Changes passive")

desc = next((r for r in class_desc if r["Name"] == "QTD_SeventyTwoChanges"), None)
if not desc:
    errors.append("Missing QTD_SeventyTwoChanges ClassDescriptions row")
else:
    if desc.get("ParentUUID") != "db08d3bc-52c1-4141-a7fb-65bc4a2a155f":
        errors.append("Seventy-Two Changes ParentUUID mismatch")
    if desc.get("ProgressionTableUUID") != "4d2f7b28-c2a8-4bde-9df1-04e2e6c6c1b5":
        errors.append("Seventy-Two Changes ProgressionTableUUID mismatch")

required_stats = (
    'new entry "QTD_Passive_SeventyTwoChanges_L3"',
    'UnlockSpell(QTD_Transform_Spider,AddChildren,1f3a673b-dc8b-4eca-9097-c6605a3de947)',
    'new entry "QTD_Passive_SeventyTwoChanges_L6"',
    'UnlockSpell(QTD_Transform_Panther,AddChildren,1f3a673b-dc8b-4eca-9097-c6605a3de947)',
    'new entry "QTD_Passive_SeventyTwoChanges_L10"',
    'UnlockSpell(QTD_Transform_Owlbear,AddChildren,1f3a673b-dc8b-4eca-9097-c6605a3de947)',
    'UnlockSpell(QTD_Transform_Dilophosaurus,AddChildren,1f3a673b-dc8b-4eca-9097-c6605a3de947)',
    'using "Shout_WildShape_Combat_Spider"',
    'using "Shout_WildShape_Combat_Panther"',
    'using "Shout_WildShape_Combat_Owlbear"',
    'using "Shout_WildShape_Combat_Dilophosaurus"',
    'using "WILDSHAPE_SPIDER_GIANT_PLAYER"',
    'using "WILDSHAPE_PANTHER_PLAYER"',
    'using "WILDSHAPE_OWLBEAR_PLAYER_10"',
    'using "WILDSHAPE_DILOPHOSAURUS_PLAYER"',
    'UseCosts" "BonusActionPoint:1;QTD_SageQi:1"',
    'UseCosts" "BonusActionPoint:1;QTD_SageQi:2"',
    'UseCosts" "BonusActionPoint:1;QTD_SageQi:3"',
    'ApplyStatus(OWLBEAR_WILDSHAPE_RAGE,100,-1)',
)
for token in required_stats:
    if token not in stats:
        errors.append(f"Missing Stats token: {token}")

if stats.count('data "SpellContainerID" "QTD_TransformContainer"') != 4:
    errors.append("All 4 subclass forms must use QTD_TransformContainer")
if stats.count('data "Requirements" ""') != 4:
    errors.append("All 4 subclass forms must clear inherited Requirements")
if stats.count('data "RequirementEvents" ""') != 4:
    errors.append("All 4 subclass forms must clear inherited RequirementEvents")
if stats.count('data "RequirementConditions" "not HasStatus(\'QTD_STATUS_FATIAN_XIANG_DI\')"') != 4:
    errors.append("All 4 subclass forms must carry the Fa Tian mutual-exclusion gate")

for forbidden in (
    'new entry "Shout_WildShape_Combat_Spider"',
    'new entry "Shout_WildShape_Combat_Panther"',
    'new entry "Shout_WildShape_Combat_Owlbear"',
    'new entry "Shout_WildShape_Combat_Dilophosaurus"',
    'new entry "WILDSHAPE_SPIDER_GIANT_PLAYER"',
    'new entry "WILDSHAPE_PANTHER_PLAYER"',
    'new entry "WILDSHAPE_OWLBEAR_PLAYER_10"',
    'new entry "WILDSHAPE_DILOPHOSAURUS_PLAYER"',
):
    if forbidden in stats:
        errors.append(f"Subclass must not override vanilla entry: {forbidden}")

for token in (
    "tech_name: QTD_SeventyTwoChanges",
    "role: transformation_control",
    "progression_type: 1",
    "create_second_container: false",
    "no_global_sage_qi_cost_reduction: true",
    "do_not_override_vanilla_wildshape: true",
    "no_script_extender_required: true",
):
    if token not in spec:
        errors.append(f"Missing subclass spec token: {token}")

if "tech_name: QTD_SeventyTwoChanges" not in subclasses or "status: subclass-wired-draft" not in subclasses:
    errors.append("data/subclasses.yaml must mark Seventy-Two Changes as wired draft")

for key in (
    "QTD_SeventyTwoChanges_DisplayName",
    "QTD_Passive_SeventyTwoChanges_L3_DisplayName",
    "QTD_Passive_SeventyTwoChanges_L6_DisplayName",
    "QTD_Passive_SeventyTwoChanges_L10_DisplayName",
    "QTD_Transform_Spider_DisplayName",
    "QTD_Transform_Panther_DisplayName",
    "QTD_Transform_Owlbear_DisplayName",
    "QTD_Transform_Dilophosaurus_DisplayName",
):
    if key not in loc:
        errors.append(f"Missing localization key: {key}")

for line in (
    "Subclass,QTD_SeventyTwoChanges,V0.3,subclass-wired-draft",
    "Transform,QTD_Transform_Spider,V0.3,base-chain-aligned",
    "Transform,QTD_Transform_Panther,V0.3,base-chain-aligned",
    "Transform,QTD_Transform_Owlbear,V0.3,base-chain-aligned",
    "Transform,QTD_Transform_Dilophosaurus,V0.3,base-chain-aligned",
):
    if line not in impl:
        errors.append(f"Missing implementation status: {line}")

uuid_keys = (
    "subclass_seventy_two_changes_table_uuid",
    "subclass_seventy_two_changes_classdesc_uuid",
    "subclass_seventy_two_changes_l3_uuid",
    "subclass_seventy_two_changes_l6_uuid",
    "subclass_seventy_two_changes_l10_uuid",
    "passive_seventy_two_changes_l3_uuid",
    "passive_seventy_two_changes_l6_uuid",
    "passive_seventy_two_changes_l10_uuid",
    "spell_transform_spider_uuid",
    "spell_transform_panther_uuid",
    "spell_transform_owlbear_uuid",
    "spell_transform_dilophosaurus_uuid",
    "status_transform_spider_uuid",
    "status_transform_panther_uuid",
    "status_transform_owlbear_uuid",
    "status_transform_dilophosaurus_uuid",
)
for key in uuid_keys:
    value = manifest.get("uuids", {}).get(key)
    if not value:
        errors.append(f"Missing UUID manifest key: {key}")
    else:
        try:
            uuid.UUID(value)
        except Exception:
            errors.append(f"Invalid UUID manifest value: {key}={value}")

if errors:
    print("SEVENTY-TWO CHANGES SUBCLASS VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("SEVENTY-TWO CHANGES SUBCLASS VALIDATION OK")
print("Validated subclass L3/L6/L10 progression + shared transform container + Spider/Panther/Owlbear/Dilophosaurus inherited chains.")
print("Runtime readiness: SUBCLASS-WIRED-DRAFT; local Patch 8 Toolkit validation still required.")
