# V0.1 Toolkit Clone Matrix

这份清单把 V0.1 中仍需 BG3 Toolkit 实机确认的对象，绑定到可搜索的原版记录或官方已确认的 Stats/Functor 模式。目标是逐个拔掉 `TODO_TOOLKIT_CLONE_*`，而不是凭记忆填写内部 ID。

## 1. 筋斗云 / `Target_QTD_SomersaultCloud`

- **类型**：Target SpellData
- **行为参考**：`Target_MistyStep`
- **已确认**：官方文档中存在 `Target_MistyStep`；`TeleportSource()` 是官方 Functor，用于把施法者传送到目标位置。
- **当前草案**：继承 `Target_MistyStep`，覆盖消耗、距离、名称，并使用 `TeleportSource()`。
- **Toolkit 要做**：
  1. Shared/GustavDev → SpellData → Target 搜索 `MistyStep`。
  2. 对比/复制目标地面选择、路径校验、SpellFlags、动画与 VFX 字段。
  3. 将范围设为 12m。
  4. 验证 `BonusActionPoint:1;QTD_SageQi:1`。
  5. 找一个“对施法者应用 1 回合状态”的可靠模式，再追加 `QTD_STATUS_CLOUD_MOMENTUM`。
- **验收**：能选择空地；传送一次；正确扣 1 Bonus Action + 1 仙力；不允许落到非法位置。

## 2. 定海一棒 / `Zone_QTD_SeaCalmingStrike`

- **类型**：Zone SpellData
- **字段参考**：官方职业教程确认 `Zone_BurningHands` 是有效 Zone TechName，可用于查 Zone 表字段布局，但不建议直接继承其锥形几何。
- **已确认 Functor/语法**：
  - `not SavingThrow(Ability.Strength, SourceSpellDC())`
  - `DealDamage(...)`
  - `ApplyStatus(PRONE,100,1)`
  - `Force(3,OriginToEntity,Aggressive,true)`
- **当前草案**：STR Save；失败 2d8 Thunder + Prone + 3m Force；成功半伤。
- **Toolkit 要做**：
  1. 在 Zone SpellData 找一个以施法者为中心/近身范围的原版技能作几何与动画参考。
  2. 确认 `TargetRadius`/`AreaRadius`/Zone shape 的实际字段组合。
  3. 验证 Force 方向是从中心向外。
  4. 再寻找原版“武器动作/主手武器伤害”实现，决定如何加入目标设计中的 Weapon Damage。
- **验收**：敌人做 STR Save；失败倒地并向外击退；成功不倒地不击退；双方都按设计承受雷鸣伤害。

## 3. 火眼金睛 / `Target_QTD_FieryGoldenEyes`

- **类型**：Target SpellData + StatusData
- **当前安全部分**：`ApplyStatus(QTD_STATUS_DEMON_REVEALED,100,3)`。
- **Toolkit 要做**：
  1. 查找 See Invisibility/显形类技能或状态的原版记录。
  2. 验证阻止再次隐形的 Boost/Status 组合。
  3. AC -2 可以保留为状态 Boost，但需在 Toolkit 中确认字段序列化。
  4. “仅悟空攻击该目标获得 Advantage”暂不实现为全局状态，必须找到 attacker-specific 条件模式后再启用。

## 4. 如意金箍棒 / `WPN_QTD_RuyiJinguBang`

- **类型**：Weapon
- **Toolkit 要做**：
  1. GustavDev → Weapon 搜索 Quarterstaff，选择一个最普通、最少附加逻辑的棍类 Parent。
  2. 用实际 Parent 名替换 `TODO_TOOLKIT_CLONE_QUARTERSTAFF_TEMPLATE`。
  3. 确认 versatile 一手/双手伤害继承正常。
  4. 保留 +2 与 Force 附伤设计，逐项验证 Boost 名称。
  5. `Target_QTD_RuyiExtend` 的远距离武器命中逻辑后续从原版 Weapon Action 克隆。

## 5. 锁子黄金甲 / `ARM_QTD_GoldenArmor`

- **类型**：Armor
- **官方路径**：Stats Editor → Armor；必须填写 `RootTemplate`、`Name`、`Parent`。Parent 可从 GustavDev Armor 浏览。
- **Toolkit 要做**：选择一个视觉和护甲类型合适的 Parent，V0.1 先复用现有 RootTemplate/mesh。

## 6. 藕丝步云履 / `BOOTS_QTD_CloudWalking`

- **类型**：Armor/Boots
- **推荐参考**：官方职业教程使用 `ARM_Boots_Leather` 作为起始靴子示例，因此它是可确认存在的基础靴 TechName，可作为低逻辑 Parent 搜索起点。
- **Toolkit 要做**：先验证 Movement 与 Jump Boost；“短休一次免费筋斗云”留到找到稳定的 UnlockSpell + cooldown 模式后再启用。

## 7. 起始装备 / `EQP_CC_QTD_GreatSage`

- Stats Editor → Equipment。
- `Initial Weapon Set = Melee`。
- 添加金箍棒、黄金甲、步云履。
- 在主职业 `ClassDescriptions.ClassEquipment` 填 `EQP_CC_QTD_GreatSage`。
- 只挂主职业，不挂未来子职业。

## 完成标准

一个条目只有在以下条件全部满足后，才能从 `stats-draft` 升级为 `toolkit-verified`：

1. 原版 Parent/参考对象已在用户本机 Toolkit 中找到。
2. 字段已复制或录入到 QitianDasheng 工程。
3. `Basic_Level_A` 成功执行。
4. 游戏日志中没有该对象相关 Stats/UUID 错误。
5. 至少完成一次实际战斗验证。
