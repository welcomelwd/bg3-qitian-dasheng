# Starting Equipment

Create an Equipment table in BG3 Toolkit Stats Editor.

Planned entry:

- Name: `EQP_CC_QTD_GreatSage`
- Planning UUID: `3dc9d807-9227-4cbb-a5c1-47c868b6af12`
- Initial Weapon Set: `Melee`
- Item 1: `WPN_QTD_RuyiJinguBang`
- Item 2: `ARM_QTD_GoldenArmor`
- Item 3: `BOOTS_QTD_CloudWalking`

Then set the main `QTD_GreatSage` ClassDescriptions row `ClassEquipment` field to `EQP_CC_QTD_GreatSage`.

Do not attach the equipment row to future subclass ClassDescriptions entries.

## RootTemplate recording

Use `data/toolkit_item_recording.csv` as the authoritative handoff sheet between repository planning IDs and Toolkit-created objects.

For the Ruyi Jingu Bang V0.1 pass:

- Stats parent: `WPN_Quarterstaff`
- Vanilla RootTemplate clone source: `96e2abaf-78ff-4dcb-a6a3-a5f0c348bd9f`
- Planned custom root: `521284c4-3d7b-4642-9c26-3677198f5a69`
- Custom root `Stats` must point to `WPN_QTD_RuyiJinguBang`
- Reuse vanilla Quarterstaff visual / physics / equipment type in V0.1

If Toolkit generates a different UUID, Toolkit wins. Update `data/toolkit_item_recording.csv`, `data/uuid_manifest.json`, and the corresponding Stats `RootTemplate` field together.

Golden Armour and Cloud-Walking Boots keep their clone-source fields pending until their dedicated equipment passes.
