# BG3 Toolkit 实施说明

## 重要原则

本仓库当前阶段存的是 **Toolkit 录入规格**，不是宣称可直接加载的手写 LSX。BG3 Toolkit 会自动生成大量对象 UUID 和资源引用，实际生成值优先于规划值。

## 1. 创建 Mod

- Mod Name: `QitianDasheng`
- Namespace / 前缀: `QTD`
- 规划 Mod UUID: `81c36a70-ea93-4375-91d7-74ae0053346d`

## 2. Progressions

在 UUID Object Editor 中为 Mod 创建 `Progressions` 表。

- 主职业 `ProgressionType = 0`
- Level 1–12 共用同一个 `TableUUID`
- 每一等级行使用独立 UUID
- 规划 TableUUID: `8b1758f9-46a7-4865-8c49-d7283fb5f456`
- 逐行数据见 `data/progressions.csv`

注意：官方文档明确要求同一职业各等级共享 TableUUID，且每个 progression 行 UUID 唯一。

## 3. ClassDescriptions

创建 `ClassDescriptions` 表，按 `data/class_descriptions.csv` 录入。关键字段：

- Name: `QTD_GreatSage`
- Primary Ability: `Strength`
- Spell Casting Ability: `Wisdom`
- Learning Strategy: `AllChildren`
- Must Prepare Spells: `No`
- Can Learn Spells: `No`
- BaseHp: `10`
- HPPerLevel: `6`
- Hotbar Columns: `9 / 5 / 2`
- ClassEquipment: `EQP_CC_QTD_GreatSage`

另建一条 `IsMulticlass = Yes` 的 Level 1 描述行，并保证 UUID 不同。

## 4. 仙力资源

创建自定义 Action Resource：`QTD_SageQi`。

设计目标：
- L1 2 点
- L2 +1
- L5 +1
- L8 +1
- L11 +1
- 短休全部恢复

`data/progressions.csv` 使用 `ActionResource(QTD_SageQi,...)` 作为规划表达式。**最终参数形式必须以当前 Toolkit 实际序列化结果为准**，不要仅凭文本规格硬写入 LSX。

## 5. SpellLists

创建三组 SpellList：

- L2：`Shout_QTD_SomersaultCloud`
- L3：`Zone_QTD_SeaCalmingStrike`
- L6：`Target_QTD_FieryGoldenEyes`

然后在 Progression 的 `Selectors` 中使用 `AddSpells(<SpellList UUID>)`。规划 UUID 位于 `data/spell_lists.csv`。

## 6. Passives / Spells / Statuses

按照 `data/passives.yaml`、`data/spells.yaml`、`data/statuses.yaml` 实现。优先在 Toolkit 中克隆最接近的原版行为，再改为 `QTD_` Tech Name。这样可以降低因猜测内部 Boost/Functor 名称导致的失效风险。

## 7. Starting Equipment

创建 Equipment 行：`EQP_CC_QTD_GreatSage`。V0.1 先绑定金箍棒和轻量化占位装备。完成物品 Stats 后，再把 ClassDescriptions 的 `ClassEquipment` 指向该行。

## 8. 图标

职业图标名与 ClassDescriptions 的 Name 保持一致：`QTD_GreatSage`。

目录：

```text
Data/Mods/QitianDasheng/GUI/Assets/ClassIcons
Data/Mods/QitianDasheng/GUI/AssetsLowRes/ClassIcons
Data/Mods/QitianDasheng/GUI/Assets/ClassIcons/hotbar
Data/Mods/QitianDasheng/GUI/AssetsLowRes/ClassIcons/hotbar
```

## 9. 快速测试

1. 加载 `Basic_Level_A`。
2. 切换 Game Mode。
3. 对角色使用 `Ctrl+Shift+L` 快速升级。
4. 检查职业是否可选、多职业入口是否出现。
5. 逐级检查 1–12 级奖励。
6. 完成后 `Publish Local`，再开正式新档回归。
