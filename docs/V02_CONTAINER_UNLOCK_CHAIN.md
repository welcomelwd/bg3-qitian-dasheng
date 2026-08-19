# V0.2 Container + Unlock Passive Chain

This document records the current implementation plan for delivering 七十二变 through one linked spell container.

## Why this pattern

Current BG3 Stats examples use linked spell containers with:

- parent `ContainerSpells`
- child `SpellContainerID`
- parent `SpellFlags = IsLinkedSpellContainer`

Current Wild Shape-derived Stats also contain `UnlockSpell(<spell>,AddChildren,<GUID>)`, which allows a passive/status to add a spell into an existing container.

For Qitian Dasheng this is preferable to putting all forms directly on the hotbar or relying on unverified passive-based `RequirementConditions`.

## QTD chain

Container TechName:

`QTD_TransformContainer`

Planning container UUID:

`1f3a673b-dc8b-4eca-9097-c6605a3de947`

Level 3 grants `QTD_Passive_TransformUnlock_L3`.

Its Boosts:

`UnlockSpell(QTD_TransformContainer);UnlockSpell(QTD_Transform_Insect,AddChildren,1f3a673b-dc8b-4eca-9097-c6605a3de947)`

Level 5 grants `QTD_Passive_TransformUnlock_L5`.

Its Boosts:

`UnlockSpell(QTD_Transform_Eagle,AddChildren,1f3a673b-dc8b-4eca-9097-c6605a3de947);UnlockSpell(QTD_Transform_Tiger,AddChildren,1f3a673b-dc8b-4eca-9097-c6605a3de947)`

Resulting UX:

- L1-L2: no 七十二变 button.
- L3-L4: one 七十二变 button containing 小虫变化.
- L5+: the same button contains 小虫、苍鹰、猛虎.

## Inherited Wild Shape gating

Each QTD child inherits a known-good vanilla Wild Shape spell for animation/behavior, but explicitly overrides:

- `UseCosts`
- `Requirements`
- `RequirementConditions`
- `RequirementEvents`

This is intentional. It prevents inherited Druid/WildShape resource gates from making a QTD form unusable even when Sage Qi is available.

## Toolkit verification gate

The AddChildren GUID must match the actual container UUID generated/assigned by the user's local Patch 8 Toolkit.

If Toolkit does not use `1f3a673b-dc8b-4eca-9097-c6605a3de947`:

1. update `data/uuid_manifest.json`
2. update both transform unlock passives
3. update `data/transforms.yaml`
4. update `scripts/validate_transform_specs.py`
5. retest Level 3 and Level 5 in `Basic_Level_A`

Do not mark this chain `toolkit-verified` until the menu changes from one child at L3 to three children at L5 in an actual game session.
