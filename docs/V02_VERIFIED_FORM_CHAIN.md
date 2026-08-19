# V0.2 Verified Wild Shape Chain

本文件记录七十二变前三个原型已经确认的 BG3 Wild Shape 数据链。

## 数据来源

主要交叉参考：

- Yoonmoonsik/bg3dnd：公开完整 BG3 Toolkit/Stats 工程，包含 Patch 8 时代的 `Spell_Shout.txt`、`Status_POLYMORPHED.txt` 与 `Shapeshift/Rulebook.lsx`。
- NellsRelo/bg3-schema：公开 BG3 Stats/Static Data schema，用于确认 `POLYMORPHED`、SpellData、StatusData 字段语义。
- crazyace/bg3-forge：Patch 8 retail-validated 数据读取/查询工具。最终本机验证推荐使用它查询用户实际安装的 BG3 数据。

注意：公开模组可能覆盖部分 vanilla 字段，因此这些记录用于确定 **TechName、继承关系、TemplateID、Rules 与实现模式**。发布前仍以用户本机 Patch 8 Toolkit / game data 为最终真值。

## 小虫变化（Phase 1 使用 Cat 技术模板）

### Base spell

`Shout_WildShape_Combat_Cat`

已观察到的有效 override 模式：

```text
SpellProperties = ApplyStatus(WILDSHAPE_CAT_PLAYER,100,-1)
```

### Base polymorph status

`WILDSHAPE_CAT_PLAYER`

- StatusType: `POLYMORPHED`
- Parent: `WILDSHAPE_BADGER_PLAYER`
- StackId: `WILDSHAPE`
- TemplateID: `398887ea-5013-4c9b-8f89-37f44efef8dc`
- Rules: `9c580a1d-dab9-4b17-b0da-b16c7d7360e0`
- Dismiss: inherited Boost includes `UnlockSpell(Shout_WildShape_Dismiss)`
- Notable behavior: half fall damage

QTD implementation:

```text
QTD_Transform_Insect
  using Shout_WildShape_Combat_Cat
  -> ApplyStatus(QTD_POLYMORPH_INSECT)

QTD_POLYMORPH_INSECT
  using WILDSHAPE_CAT_PLAYER
```

Phase 1 的目标是验证变身、回退、Hotbar、装备恢复与小体型链路。真正昆虫视觉放到 Phase 2。

## 苍鹰变化（Phase 1 使用 Dire Raven 技术模板）

### Base spell

`Shout_WildShape_Combat_Raven`

```text
SpellProperties = ApplyStatus(WILDSHAPE_RAVEN_PLAYER,100,-1)
```

### Base polymorph status

`WILDSHAPE_RAVEN_PLAYER`

- StatusType: `POLYMORPHED`
- Parent: `WILDSHAPE_BADGER_PLAYER`
- StackId: `WILDSHAPE`
- TemplateID: `6c2fc745-20b3-44c0-9032-97e97a5368eb`
- Rules: `9c580a1d-dab9-4b17-b0da-b16c7d7360e0`
- Dismiss: `UnlockSpell(Shout_WildShape_Dismiss)`
- Movement: `ActionResource(Movement,3,0)`
- Flight-related behavior: `Attribute(Floating)` + `IgnoreFallDamage()`

QTD implementation:

```text
QTD_Transform_Eagle
  using Shout_WildShape_Combat_Raven
  -> ApplyStatus(QTD_POLYMORPH_EAGLE)

QTD_POLYMORPH_EAGLE
  using WILDSHAPE_RAVEN_PLAYER
```

第一阶段先接受 Raven 外观，确认飞行/垂直导航完全稳定，再尝试替换 Giant Eagle RootTemplate。

## 猛虎变化

### Base spell

注意原版 TechName 大小写：

`Shout_Wildshape_Combat_SaberTooth_Tiger`

```text
SpellProperties = ApplyStatus(WILDSHAPE_SABERTOOTH_TIGER_PLAYER,100,-1)
```

### Base polymorph status

`WILDSHAPE_SABERTOOTH_TIGER_PLAYER`

- StatusType: `POLYMORPHED`
- Parent: `WILDSHAPE_BADGER_PLAYER`
- StackId: `WILDSHAPE`
- TemplateID: `007a0a64-d763-4daf-9697-21765a4c2d4d`
- Rules: `9c580a1d-dab9-4b17-b0da-b16c7d7360e0`
- OnApply: applies `REGENERATION_SABERTOOTH` and `WILDSHAPE_ACTIVE`
- OnRemove: removes regeneration, applies Wild Shape technical cleanup, removes active marker
- Dismiss: inherited from base Wild Shape status

QTD implementation:

```text
QTD_Transform_Tiger
  using Shout_Wildshape_Combat_SaberTooth_Tiger
  -> ApplyStatus(QTD_POLYMORPH_TIGER)

QTD_POLYMORPH_TIGER
  using WILDSHAPE_SABERTOOTH_TIGER_PLAYER
```

## Shared Wild Shape rule

三个 base player statuses 均使用：

`WildShapeKeepName`

UUID:

`9c580a1d-dab9-4b17-b0da-b16c7d7360e0`

观察到的关键行为：

- ApplySpellsFromTemplate = true
- ApplyTagsFromTemplate = true
- ApplyVisual = true
- BaseACOverride = true
- ChangeAi = true
- ChangeRace = true
- DisableEquipmentSlots = true
- RemoveOldTags = true
- RemovePrevSpells = true
- RetainDisplayName = true
- UnarmedAbilityFromTemplate = true
- WildShapeHotBar = true
- Scale / Weight 使用 template 值

这解释了为什么 QTD 最安全的做法是继承成熟 Wild Shape status，而不是重新手写整套 polymorph rule。

## 本机最终验证

推荐在安装 BG3 的 Windows 开发机使用 BG3 Forge：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install "bg3forge[all]==0.2.0"
bg3forge doctor

bg3forge lookup Shout_WildShape_Combat_Cat
bg3forge lookup WILDSHAPE_CAT_PLAYER
bg3forge lookup Shout_WildShape_Combat_Raven
bg3forge lookup WILDSHAPE_RAVEN_PLAYER
bg3forge lookup Shout_Wildshape_Combat_SaberTooth_Tiger
bg3forge lookup WILDSHAPE_SABERTOOTH_TIGER_PLAYER
```

然后在 Toolkit 中对照 Shared / GustavDev 的实际字段。如果 inherited spell 仍包含 `WildShape` 资源 Requirement，QTD 子条目必须显式覆盖对应 Requirements；仅替换 `UseCosts` 不一定足够。

## Runtime gate

只有完成以下项目，三个形态才从 `base-chain-aligned` 升为 `toolkit-verified`：

1. 本机数据查询与本文 TechName/TemplateID/Rules 一致。
2. QTD_SageQi 能替代 inherited WildShape cost，且没有隐藏资源 Requirements。
3. Dismiss Wild Shape 正常。
4. 0 HP 正常恢复原形。
5. 装备、Hotbar、状态正常恢复。
6. Cat/Raven/Sabre-Tooth 各完成一次正式游戏测试。
