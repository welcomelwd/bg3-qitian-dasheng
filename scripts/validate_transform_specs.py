#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
transforms = (ROOT / "data" / "transforms.yaml").read_text(encoding="utf-8")
spells = (ROOT / "src" / "stats" / "Transforms.txt").read_text(encoding="utf-8")
statuses = (ROOT / "src" / "stats" / "TransformStatuses.txt").read_text(encoding="utf-8")

expected = {
    "QTD_Transform_Insect": {
        "base_spell": "Shout_WildShape_Combat_Cat",
        "qtd_status": "QTD_POLYMORPH_INSECT",
        "base_status": "WILDSHAPE_CAT_PLAYER",
        "template": "398887ea-5013-4c9b-8f89-37f44efef8dc",
    },
    "QTD_Transform_Eagle": {
        "base_spell": "Shout_WildShape_Combat_Raven",
        "qtd_status": "QTD_POLYMORPH_EAGLE",
        "base_status": "WILDSHAPE_RAVEN_PLAYER",
        "template": "6c2fc745-20b3-44c0-9032-97e97a5368eb",
    },
    "QTD_Transform_Tiger": {
        "base_spell": "Shout_Wildshape_Combat_SaberTooth_Tiger",
        "qtd_status": "QTD_POLYMORPH_TIGER",
        "base_status": "WILDSHAPE_SABERTOOTH_TIGER_PLAYER",
        "template": "007a0a64-d763-4daf-9697-21765a4c2d4d",
    },
}

errors = []
for tech_name, ref in expected.items():
    if tech_name not in transforms:
        errors.append(f"Missing transform spec: {tech_name}")
    if f'new entry "{tech_name}"' not in spells:
        errors.append(f"Missing transform SpellData draft: {tech_name}")
    if f'using "{ref["base_spell"]}"' not in spells:
        errors.append(f"Missing base spell inheritance for {tech_name}: {ref['base_spell']}")
    if f'ApplyStatus({ref["qtd_status"]},100,-1)' not in spells:
        errors.append(f"Missing QTD polymorph application for {tech_name}: {ref['qtd_status']}")
    if f'new entry "{ref["qtd_status"]}"' not in statuses:
        errors.append(f"Missing QTD polymorph status: {ref['qtd_status']}")
    if f'using "{ref["base_status"]}"' not in statuses:
        errors.append(f"Missing base status inheritance: {ref['base_status']}")
    if ref["template"] not in transforms and ref["template"] not in statuses:
        errors.append(f"Missing reference TemplateID for {tech_name}: {ref['template']}")

required_policy = (
    "overwrite_vanilla_wildshape: false",
    "never_override_shared_wildshape_spell: true",
    "never_override_shared_polymorph_status: true",
    "required_status_group: SG_Polymorph_BeastShape",
    "shared_rules_uuid: 9c580a1d-dab9-4b17-b0da-b16c7d7360e0",
    "final_truth_is_local_patch8_toolkit: true",
)
for policy in required_policy:
    if policy not in transforms:
        errors.append(f"Missing compatibility policy: {policy}")

for forbidden in (
    'new entry "WILDSHAPE_CAT_PLAYER"',
    'new entry "WILDSHAPE_RAVEN_PLAYER"',
    'new entry "WILDSHAPE_SABERTOOTH_TIGER_PLAYER"',
    'new entry "Shout_WildShape_Combat_Cat"',
    'new entry "Shout_WildShape_Combat_Raven"',
    'new entry "Shout_Wildshape_Combat_SaberTooth_Tiger"',
):
    if forbidden in spells or forbidden in statuses:
        errors.append(f"QTD must not override vanilla entry: {forbidden}")

if errors:
    print("TRANSFORM SPEC VALIDATION FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("TRANSFORM SPEC VALIDATION OK")
print("Validated 3 QTD transform spells and 3 inherited polymorph statuses.")
print("Runtime readiness: BASE-CHAIN-ALIGNED; local Patch 8 Toolkit verification still required.")
