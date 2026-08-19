# V0.2 Hair Clone Architecture

## Goal

Implement **身外身法 / Hair Clones** as a stable no-Script-Extender prototype before attempting true runtime duplication of the player character.

## V0.2 prototype

- Unlock: Great Sage level 6
- TechName: `Target_QTD_HairClones`
- Cost: Bonus Action + 3 Sage Qi
- Count: 2 controlled summons
- Lifetime: 3 rounds
- Recast: replaces the previous pair through two unique Stack IDs
- Runtime inventory cloning: disabled
- Story/origin character templates: forbidden
- Script Extender: not required for the base prototype

## Summon chain

```text
Target_QTD_HairClones
  ├─ GROUND:Summon(QTD_HairClone_Root_L6, 3, ..., 'QTD_HairClone_A', QTD_STATUS_HAIR_CLONE, ..., UseCasterPassives=true)
  └─ GROUND:Summon(QTD_HairClone_Root_L6, 3, ..., 'QTD_HairClone_B', QTD_STATUS_HAIR_CLONE, ..., UseCasterPassives=true)

QTD_HairClone_Root_L6
  └─ Stats = QTD_HairCloneCharacter_L6
       ├─ fixed HP/AC/abilities
       ├─ weak quarterstaff assigned in Toolkit
       └─ no Extra Attack in first prototype
```

Planning RootTemplate UUID: `8c17bf83-fc1d-4143-b555-46b38003bb49`.

The UUID above is a project planning value. The local Toolkit object is authoritative. If Toolkit generates another UUID, update `data/uuid_manifest.json`, `data/hair_clones.yaml`, `src/stats/HairClones.txt`, and the validator together.

## Why fixed stats first

True cloning of current HP, equipment, appearance, arbitrary passives and unique-item state is substantially more fragile than a normal summon. A fixed RootTemplate gives us a clean first test for:

1. summon ownership and player control,
2. two simultaneous summons,
3. 3-round cleanup,
4. recast replacement,
5. combat turn participation,
6. staff animation and attacks,
7. caster-death unsummon behavior.

Once these work, we can decide whether dynamic duplication merits BG3 Script Extender.

## Collision fallback

The first draft executes two `Summon()` functors on the same selected ground point. If local Toolkit testing shows collision/pathing failures, convert the action into a linked container with two child target spells so the player selects two nearby positions. Do not solve this with unverified positioning syntax.

## Balance

L6 clone stat target:

- HP 24
- AC 14
- STR 16 / DEX 16
- one normal action, one bonus action, one reaction
- no Extra Attack
- weak quarterstaff, no legendary item passives

Future candidates:

- L9: improve HP or clone weapon, not both aggressively.
- L12: allow four weaker clones, with total damage kept close to the upgraded two-clone version.

## Toolkit validation checklist

- Create `QTD_HairClone_Root_L6`.
- Set Stats to `QTD_HairCloneCharacter_L6`.
- Verify `CanStand()` with the final RootTemplate UUID.
- Assign a weak quarterstaff.
- Confirm both Stack IDs can coexist.
- Confirm recast replaces both old clones.
- Confirm each clone expires after exactly 3 rounds.
- Confirm caster death unsummons them.
- Confirm `bUseCasterPassives=true` causes no unintended passive loops.
- Verify multiplayer with two Great Sage characters before declaring the Stack IDs safe.
