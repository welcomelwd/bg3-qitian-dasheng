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
- Weapon: one shared `WPN_QTD_HairCloneStaff` that scales from the summoned clone's own Character level

## Level scaling

| Great Sage level | Character Stats | HP | AC | STR | DEX | CON | Extra Attack |
|---|---|---:|---:|---:|---:|---:|---|
| 6-7 | `QTD_HairCloneCharacter_L6` | 24 | 14 | 16 | 16 | 12 | No |
| 8-9 | `QTD_HairCloneCharacter_L8` | 32 | 15 | 18 | 18 | 12 | No |
| 10-11 | `QTD_HairCloneCharacter_L10` | 40 | 16 | 18 | 18 | 14 | No |
| 12 | `QTD_HairCloneCharacter_L12` | 48 | 17 | 20 | 20 | 14 | No |

The clones intentionally never gain Extra Attack in this V0.2 track. Their number, duration and Sage Qi cost also stay fixed, so scaling improves survivability and accuracy/damage without multiplying the action economy.

## Clone weapon scaling

All four clone RootTemplates equip the same item RootTemplate: `QTD_HairCloneStaff_Root` (planning UUID `757f581b-683f-40ac-8051-47c10ef651a2`). Its Stats entry is `WPN_QTD_HairCloneStaff`, inherited from the vanilla `WPN_Quarterstaff`.

| Clone level | Weapon result |
|---|---|
| 6-7 | +0 magical quarterstaff |
| 8-9 | +1 magical quarterstaff |
| 10-11 | +1 magical quarterstaff + 1d4 Force |
| 12 | +2 magical quarterstaff + 1d4 Force |

The weapon uses conditional `DefaultBoosts` driven by the summoned clone's Character level. This pattern is used by existing BG3 weapon mods and keeps the equipment graph small: one Weapon Stats entry and one item RootTemplate instead of four copies.

`WPN_QTD_HairCloneStaff` explicitly clears the base quarterstaff's `PassivesOnEquip` so the clones do not inherit Weapon Mastery: Topple. It also does not receive Ruyi Extension, the real Jingu Bang's Strength bonus, jump bonus, or any active legendary weapon skill.

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

Shared equipment
  QTD_HairCloneStaff_Root
  UUID 757f581b-683f-40ac-8051-47c10ef651a2
  -> WPN_QTD_HairCloneStaff
```

All four character RootTemplates should use the same visual family, collision footprint and shared staff equipment. This lets `CanStand()` use the L6 template as a single placement probe.

Planning UUIDs are not authoritative. If BG3 Toolkit generates different UUIDs, update the manifest, YAML, SpellData/Weapon Stats and validator together.

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

The level-tier model gives us deterministic balance, no inventory or unique-item duplication, no Script Extender dependency, four clear test checkpoints, and simple future tuning through Character/Weapon Stats only.

## Future scope

`万千毫毛` is no longer an automatic level-12 upgrade to four summons. If added later, it should be a separate high-tier feature with its own cost and balance budget.

## Toolkit validation checklist

- Create the four `QTD_HairClone_Root_L*` templates.
- Point each RootTemplate to its matching Character Stats entry.
- Create `QTD_HairCloneStaff_Root` and set Stats to `WPN_QTD_HairCloneStaff`.
- Equip that same staff RootTemplate on all four clone RootTemplates.
- Keep all four clone RootTemplates on the same physical footprint.
- Verify the staff shows +0 / +1 / +1+1d4 Force / +2+1d4 Force at clone levels 6 / 8 / 10 / 12.
- Verify the staff does not expose Topple or Ruyi Jingu Bang active abilities.
- Verify the internal custom class token used by `ClassLevelHigherOrEqualThan`.
- Confirm exactly two clones spawn at every tier and expire after exactly 3 rounds.
- Confirm recast replaces A/B across tier boundaries.
- Confirm caster death unsummons them.
- Confirm `bUseCasterPassives=true` does not create passive loops.
- Verify multiplayer with two Great Sage characters.
