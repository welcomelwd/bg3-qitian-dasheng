# V0.2 Defense Passives

## Scope

V0.2 now defines two passive defensive milestones for the Great Sage:

- Level 7: `QTD_Passive_GreatSageEvasion`
- Level 9: `QTD_Passive_DiamondBody`

Both are intentionally no-Script-Extender features.

## Level 7: Great Sage Evasion

`QTD_Passive_GreatSageEvasion` inherits the base-game `Evasion` PassiveData:

```text
new entry "QTD_Passive_GreatSageEvasion"
type "PassiveData"
using "Evasion"
```

Public Patch 8-derived Stats show both `Monk_7_Evasion` and `Rogue_7_Evasion` inheriting `Evasion`. Reusing the same parent is preferable to reproducing its saving-throw logic manually.

Expected behavior:

- when a Dexterity saving throw normally causes half damage on success:
  - success -> zero damage,
  - failure -> half damage.

Toolkit validation must confirm the inherited base passive resolves correctly in the user's current Patch 8 data.

## Level 9: Diamond Body

`QTD_Passive_DiamondBody` is a direct Boost-based passive:

```text
Resistance(Slashing, ResistantToNonMagical)
Resistance(Piercing, ResistantToNonMagical)
Resistance(Bludgeoning, ResistantToNonMagical)
Advantage(SavingThrow, Constitution)
```

This deliberately does **not** grant full resistance to magical physical attacks.

Why:

1. it keeps the feature strong against mundane weapons and creatures,
2. magical weapons remain an answer in late-game encounters,
3. it matches the "immortal body" theme without becoming permanent Barbarian-style resistance to nearly all weapon damage,
4. every used Boost pattern exists in released/public BG3 mod data.

Public Community Library data demonstrates `ResistantToNonMagical` for Slashing, Piercing and Bludgeoning. Public Artificer item Stats demonstrate `Advantage(SavingThrow, Constitution)`.

## Progression wiring

```text
Great Sage 7
  -> QTD_Passive_GreatSageEvasion

Great Sage 9
  -> QTD_Passive_DiamondBody
```

The existing progression rows already used these TechNames; this implementation fills the previously planned passive entries.

## Balance contract

Do not add these to V0.2 without a separate balance decision:

- magical B/P/S resistance,
- immunity to Prone,
- immunity to Poison,
- universal damage reduction,
- reaction-based half damage on top of Evasion,
- extra AC.

Those can be considered later for subclass/capstone tuning, but stacking them at levels 7-9 would overload the base class defense budget.

## Toolkit test checklist

### Great Sage Evasion

- [ ] level 6 character does not have `QTD_Passive_GreatSageEvasion`
- [ ] level 7 character receives it
- [ ] successful qualifying Dexterity save takes 0 damage
- [ ] failed qualifying Dexterity save takes half damage
- [ ] non-Dexterity saves are unaffected
- [ ] ordinary attack-roll damage is unaffected

### Diamond Body

- [ ] level 8 character does not have `QTD_Passive_DiamondBody`
- [ ] level 9 character receives it
- [ ] non-magical Slashing damage is resisted
- [ ] non-magical Piercing damage is resisted
- [ ] non-magical Bludgeoning damage is resisted
- [ ] magical physical damage is not incorrectly resisted
- [ ] Constitution saving throws have Advantage
- [ ] other saving throw abilities do not gain Advantage

Only promote these passives to `toolkit-verified` after these checks pass in-game.
