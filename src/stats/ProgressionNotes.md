# Progression to Stats integration

The class progression itself remains Toolkit UUID-object data. Stats drafts provide the spell/passive records referenced by those Progressions.

Planned selectors/boost integration:

- Level 1: grant `QTD_Passive_MonkeyAgility`, `QTD_Passive_RuyiMastery`, and initial `QTD_SageQi`.
- Level 2: grant `Shout_QTD_SomersaultCloud`, `QTD_Passive_CopperHeadIronArm`, +1 Sage Qi.
- Level 3: grant `Zone_QTD_SeaCalmingStrike`.
- Level 5: Extra Attack, +1 Sage Qi.
- Level 6: grant `Target_QTD_FieryGoldenEyes`.
- Level 8: +1 Sage Qi.
- Level 11: +1 Sage Qi.

The authoritative progression UUIDs remain in `data/progressions.csv`; after Toolkit validation, replace planned references with the actual exported identifiers.
