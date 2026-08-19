#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
transforms = (ROOT / "data" / "transforms.yaml").read_text(encoding="utf-8")
stats = (ROOT / "src" / "stats" / "Transforms.txt").read_text(encoding="utf-8")

expected = {
    "QTD_Transform_Insect": "TODO_TOOLKIT_CLONE_WILDSHAPE_CAT_SPELL",
    "QTD_Transform_Eagle": "TODO_TOOLKIT_CLONE_WILDSHAPE_DIRE_RAVEN_SPELL",
    "QTD_Transform_Tiger": "TODO_TOOLKIT_CLONE_WILDSHAPE_SABRETOOTH_SPELL",
}

errors = []
for tech_name, clone_marker in expected.items():
    if tech_name not in transforms:
        errors.append(f"Missing transform spec: {tech_name}")
    if f'new entry "{tech_name}"' not in stats:
        errors.append(f"Missing transform Stats draft: {tech_name}")
    if clone_marker not in stats:
        errors.append(f"Missing safe Toolkit clone marker: {clone_marker}")

required_policy = (
    "overwrite_vanilla_wildshape: false",
    "never_override_shared_wildshape_spell: true",
    "never_override_shared_polymorph_status: true",
    "required_status_group: SG_Polymorph_BeastShape",
)
for policy in required_policy:
    if policy not in transforms:
        errors.append(f"Missing compatibility policy: {policy}")

if errors:
    print("TRANSFORM SPEC VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("TRANSFORM SPEC VALIDATION OK")
print("Validated 3 prototype transforms; runtime readiness: NO (Toolkit clone required).")
