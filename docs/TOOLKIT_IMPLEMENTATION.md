# BG3 Toolkit 实施说明

## 重要原则

本仓库当前阶段存的是 **Toolkit 录入规格**，不是宣称可直接加载的手写 LSX。BG3 Toolkit 会自动生成大量对象 UUID 和资源引用，实际生成值优先于规划值。

职业与仙力主干的逐项录入/回填入口：`docs/V01_CLASS_RESOURCE_SPINE.md`。Toolkit 实际 UUID 回填到 `data/toolkit_spine_recording.csv`。

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

注意：同一职业各等级共享 TableUUID，每个 progression 行 UUID 唯一。`AllowImprovement=Yes` 只应出现在 L4/L8/L12。

主职业关键链：

- L1：仙力 +2，灵猴身法，如意兵法
- L2：仙力 +1，铜头铁臂，L2 SpellList
- L3：L3 SpellList + 三个子职业
- L4：Feat
- L5：仙力 +1 + Extra Attack
- L6：L6 SpellList
- L7：大圣闪避
- L8：Feat + 仙力 +1
- L9：金刚不坏
- L10：三头六臂
- L11：仙力 +1；当前 forward trunk 同时接入法天象地预览
- L12：Feat + 齐天大圣封顶被动

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

另建一条 `IsMulticlass = Yes` 的描述行，并保证 UUID 与主职业行不同。两条 ClassDescriptions 都应指向同一个主职业 Progression Table。

三个子职业 ClassDescriptions 使用各自独立 Progression Table，并以主职业 ClassDescriptions UUID 为 ParentUUID。

## 4. 仙力资源

创建自定义 Action Resource：`QTD_SageQi`。

基础 Progression 目标：

- L1 = 2
- L2 = 3
- L5 = 4
- L8 = 5
- L11 = 6

当前 forward trunk 的 L12 `QTD_Passive_QitianDasheng` 再增加 2，预期总上限为 8。

资源行为：

- Short Rest 全恢复
- Long Rest 后保持满值
- 显示在 Action Resource Panel
- 0 点时需要仙力的能力不可施放
- Respec 后不得残留旧资源上限
- Multiclass 时按实际 `QTD_GreatSage` 职业等级成长

`data/progressions.csv` 使用 `ActionResource(QTD_SageQi,...)` 作为规划表达式。**最终参数形式必须以当前 Toolkit 实际序列化结果为准**，不要仅凭文本规格硬写入 LSX。

## 5. SpellLists

创建三组 SpellList：

- L2：`QTD_SpellList_L2` → `Target_QTD_SomersaultCloud`
- L3：`QTD_SpellList_L3` → `Zone_QTD_SeaCalmingStrike`
- L6：`QTD_SpellList_L6` → `Target_QTD_FieryGoldenEyes;Target_QTD_HairClones`

然后在 Progression 的 `Selectors` 中使用 `AddSpells(<SpellList UUID>)`。规划 UUID 位于 `data/spell_lists.csv`。

`Target_QTD_SomersaultCloud` 是当前 canonical Tech Name。不要恢复旧的 Shout 类型命名。

## 6. Toolkit UUID 回填

录入主职业脊柱时同步维护 `data/toolkit_spine_recording.csv`：

1. Toolkit 创建对象后填写 `ToolkitUUID`。
2. 若 Toolkit UUID 与规划 UUID 不同，以 Toolkit 为准。
3. 同一批次更新 `data/uuid_manifest.json`、`data/progressions.csv`、`data/class_descriptions.csv`、`data/spell_lists.csv` 和所有引用。
4. `LocalState` 从 `pending-toolkit-entry` 推进到 `entered-not-tested`、`basic-level-a-pass`、`combat-pass`。
5. 未完成实际验证不得标记 `toolkit-verified`。

## 7. Passives / Spells / Statuses

按照 `data/passives.yaml`、`data/spells.yaml`、`data/statuses.yaml` 实现。优先在 Toolkit 中克隆最接近的原版行为，再改为 `QTD_` Tech Name。这样可以降低因猜测内部 Boost/Functor 名称导致的失效风险。

## 8. Starting Equipment

创建 Equipment 行：`EQP_CC_QTD_GreatSage`。V0.1 先绑定金箍棒、黄金甲和步云履。完成物品 Stats/Parent/RootTemplate 后，再验证 Character Creation 初始装备链。

## 9. 图标

职业图标名与 ClassDescriptions 的 Name 保持一致：`QTD_GreatSage`。

目录：

```text
Data/Mods/QitianDasheng/GUI/Assets/ClassIcons
Data/Mods/QitianDasheng/GUI/AssetsLowRes/ClassIcons
Data/Mods/QitianDasheng/GUI/Assets/ClassIcons/hotbar
Data/Mods/QitianDasheng/GUI/AssetsLowRes/ClassIcons/hotbar
```

## 10. 快速测试

1. 加载 `Basic_Level_A`。
2. 切换 Game Mode。
3. 对角色使用 `Ctrl+Shift+L` 逐级升级。
4. 检查职业是否可选、多职业入口是否出现。
5. 逐级检查 L1–L12 奖励。
6. 检查 L3 三个子职业、L4/L8/L12 Feat、L5 Extra Attack。
7. 检查仙力 2/3/4/5/6，当前 forward trunk L12 为 8。
8. Short Rest 验证仙力恢复。
9. Respec 后重复升级和资源检查。
10. 做一次 Multiclass，确认仙力按大圣职业等级成长。
11. 完成后 `Publish Local`，再开正式新档回归。
