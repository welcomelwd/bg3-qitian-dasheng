# V0.3 Three Heads, Six Arms

## Goal

Implement **三头六臂 / Three Heads, Six Arms** as a short, expensive melee burst form without rewriting the player skeleton, adding six independent equipment slots, or requiring BG3 Script Extender.

## Player-facing design

- Unlock: Great Sage level 10
- Passive: `QTD_Passive_ThreeHeadsSixArms`
- Active: `Shout_QTD_ThreeHeadsSixArms`
- Cost: Bonus Action + 4 Sage Qi
- Duration: 3 rounds
- Active status: `QTD_STATUS_THREE_HEADS_SIX_ARMS`

While active:

- Attack actions use the `ExtraAttack_2` tier, targeting **three weapon attacks total**.
- Armour Class +2.
- Advantage on Strength saving throws.
- Advantage on Dexterity saving throws.
- Immunity to the `SG_Frightened` status group.

The form deliberately does **not** grant another `ActionPoint`. A full extra action would also enable another full spell/action and would be much stronger than the intended extra weapon attack.

## Why `ExtraAttack_2`

Public BG3-derived data shows level-11 multiattack creature templates replacing `ExtraAttack` with `ExtraAttack_2`, and the base extra-attack chain queues `EXTRA_ATTACK_2`. Public BOOST-status implementations also demonstrate assigning `ExtraAttack_2` through the StatusData `Passives` field.

That makes a temporary BOOST status a much closer fit than Haste-style ActionPoint restoration.

## Runtime structure

```text
Level 10 Progression
    ↓
QTD_Passive_ThreeHeadsSixArms
    ↓ UnlockSpell
Shout_QTD_ThreeHeadsSixArms
    ↓ Bonus Action + 4 Sage Qi
ApplyStatus(..., 3 rounds)
    ↓
QTD_STATUS_THREE_HEADS_SIX_ARMS
    ├─ Passives: ExtraAttack_2
    ├─ AC(2)
    ├─ Advantage STR saves
    ├─ Advantage DEX saves
    └─ StatusImmunity(SG_Frightened)
```

## Balance boundaries

V0.3 intentionally excludes:

- `ExtraAttack_3`
- an additional full `ActionPoint`
- a second Bonus Action
- Advantage on all six saving throws
- Magic Resistance
- physical or elemental resistance
- six real independent weapon slots
- automatic weapon duplication
- custom skeleton dependency

The character already has Great Sage Extra Attack from level 5. During this form, the `ExtraAttack_2` chain is expected to take priority and produce the third weapon attack. This interaction must be verified in Patch 8 before marking the feature runtime-ready.

## Visual plan

The mechanics and visuals are separated.

Phase 1 uses the normal player skeleton and proves combat behavior. Phase 2 can add translucent additional arms/heads or an aura effect after a known-good Toolkit effect resource is selected.

Do not block the mechanical release on custom rigging.

## Reach

The original design included additional melee reach. That is deferred in this draft because no sufficiently reliable generic reach Boost has been verified yet. Add it later only from a known-good vanilla/Toolkit pattern.

## Toolkit/game validation

Test a Great Sage at levels 9 and 10.

At level 10:

1. Confirm the passive unlocks `Shout_QTD_ThreeHeadsSixArms`.
2. Confirm activation consumes exactly Bonus Action + 4 Sage Qi.
3. Confirm the status lasts exactly 3 rounds.
4. Confirm AC increases by exactly 2.
5. Confirm Strength and Dexterity saving throws gain Advantage.
6. Confirm Constitution, Intelligence, Wisdom, and Charisma saves do not gain Advantage.
7. Confirm Frightened-group effects are blocked.
8. Confirm one Attack action gives exactly three weapon attacks total.
9. Confirm the form does not give a second full Action.
10. Confirm spellcasting still consumes its normal Action.
11. Test with Haste and Action Surge to ensure attack/action queues do not multiply unexpectedly.
12. Test entering/leaving Seventy-Two Transformations while the status is active.
13. Verify the status and active spell disappear correctly on respec if Toolkit requires explicit remove groups.

Only after these checks should implementation status move to `toolkit-verified`.
