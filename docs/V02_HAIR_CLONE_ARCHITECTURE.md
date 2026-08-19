# V0.2 Hair Clone Architecture

## Goal

Implement **身外身法 / Hair Clones** as a stable no-Script-Extender summon that grows with the Great Sage class level.

The project no longer targets 100% runtime duplication of the caster. HP, equipment, appearance and arbitrary passive state are not copied at cast time.

## V0.2 behavior

- Unlock: Great Sage level 6
- TechName: `Target_QTD_HairClones`
- Cost: Bonus Action + 3 Sage Qi
- Count: always 2 controlled summons
- Lifetime: always 3 rounds
- Recast: replaces the previous pair through `QTD_HairClone_A` / `QTD_HairClone_B`
- Script Extender: not required
- Scaling: fixed RootTemplate tiers selected by `QTD_GreatSage` class level

## Level scaling

| Great Sage level | Character Stats | HP | AC | STR | DEX | CON | Extra Attack |
|---|---|---:|---:|---:|---:|---:|---|
| 6-7 | `QTD_HairCloneCharacter_L6` | 24 | 14 | 16 | 16 | 12 | No |
| 8-9 | `QTD_HairCloneCharacter_L8` | 32 | 15 | 18 | 18 | 12 | No |
| 10-11 | `QTD_HairCloneCharacter_L10` | 40 | 16 | 18 | 18 | 14 | No |
| 12 | `QTD_HairCloneCharacter_L12` | 48 | 17 | 20 | 20 | 14 | No |

The clones intentionally never gain Extra Attack in this V0.2 track. Their number, duration and Sage Qi cost also stay fixed, so scaling improves survivability and accuracy/damage without multiplying the action economy.

## RootTemplate tiers

```text
L6-7
  QTD_HairClone_Root_L6
  UUID 8c17bf83-fc1d-4143-b555-46b38003bb49
  -> QTD_HairCloneCharacter_L6

L8-9
  QTD_HairClone_Root_L8
  UUID 122996e7-46e1-4f04-b64d-30db7c9a47ac
  -> QTD_HairCloneCharacter_L8

L10-11
  QTD_HairClone_Root_L10
  UUID 72fdc168-2ec4-45ed-a230-21df703ff6c0
  -> QTD_HairCloneCharacter_L10

L12
  QTD_HairClone_Root_L12
  UUID b3368e82-088a-46fb-b8ec-dbc5dc5d4fe0
  -> QTD_HairCloneCharacter_L12
```

All four RootTemplates should use the same visual family, collision footprint and weak-quarterstaff equipment setup. This lets `CanStand()` use the L6 template as a single placement probe.

Planning UUIDs are not authoritative. If BG3 Toolkit generates different UUIDs, update the manifest, YAML, SpellData and validator together.

## Summon selection

`Target_QTD_HairClones` uses conditional ground functors:

```text
GROUND:IF(level < 8):Summon(L6 root...)
GROUND:IF(level >= 8 and < 10):Summon(L8 root...)
GROUND:IF(level >= 10 and < 12):Summon(L10 root...)
GROUND:IF(level >= 12):Summon(L12 root...)
```

Each tier executes the same two Stack IDs, A and B. Therefore crossing a tier and recasting still replaces the old pair instead of adding another pair.

The exact condition token is drafted as `ClassLevelHigherOrEqualThan(...,'QTD_GreatSage')` and must be confirmed against the local Toolkit class identifier before release.

## Why level tiers instead of true cloning

Runtime duplication would require synchronizing changing player state such as current HP, equipment, unique items, appearance, status effects and arbitrary passives. That creates far more failure modes than this feature needs.

The level-tier model gives us:

1. deterministic balance,
2. no inventory duplication bugs,
3. no unique-item duplication,
4. no dependency on BG3 Script Extender,
5. easy testing at four checkpoints,
6. simple future tuning through Character Stats only.

## Future scope

`万千毫毛` is no longer an automatic level-12 upgrade to four summons. If added later, it should be a separate high-tier feature with its own cost and balance budget.

## Toolkit validation checklist

- Create the four `QTD_HairClone_Root_L*` templates.
- Point each RootTemplate to its matching Character Stats entry.
- Keep all four RootTemplates on the same physical footprint.
- Give each one the same weak quarterstaff equipment setup.
- Verify the internal custom class token used by `ClassLevelHigherOrEqualThan`.
- Test at Great Sage levels 6, 8, 10 and 12.
- Confirm exactly two clones spawn at every tier.
- Confirm clones expire after exactly 3 rounds.
- Confirm recast replaces A/B across tier boundaries.
- Confirm caster death unsummons them.
- Confirm `bUseCasterPassives=true` does not create passive loops.
- Verify multiplayer with two Great Sage characters.
