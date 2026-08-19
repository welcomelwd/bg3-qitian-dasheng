# V0.1 职业与仙力主干收口

目标：先把 `QTD_GreatSage + QTD_SageQi + L1–L12 Progressions` 做成可在 Patch 8 Toolkit 逐项录入、逐项回填、逐项验收的稳定主干。

> 这不是手写 LSX 发布物。`data/` 中 UUID 是规划值；BG3 Toolkit 实际生成的 UUID 永远优先。录入完成后，把实际值填入 `data/toolkit_spine_recording.csv`，再同步修改 manifest 和所有引用。

## 1. 录入顺序

严格按下面顺序做，避免先建 Progression 后再追 UUID：

1. 创建/确认 Mod `QitianDasheng`。
2. 创建 `QTD_SageQi` ActionResourceDefinitions。
3. 创建主职业 Progressions Table。
4. 创建主职业 L1–L12 的 12 条 Progression 行。
5. 创建主职业 ClassDescriptions。
6. 创建独立 Multiclass ClassDescriptions 行。
7. 创建 L2/L3/L6 三个 SpellList。
8. 创建三个子职业 ClassDescriptions 和各自 Progression Table。
9. 回到主职业 L3，确认三个子职业全部出现在 `SubClasses`。
10. 创建/绑定 `EQP_CC_QTD_GreatSage` 后再做 Character Creation 测试。

## 2. 主职业固定规格

`QTD_GreatSage`：

- Primary Ability: `Strength`
- Spell Casting Ability: `Wisdom`
- Learning Strategy: `AllChildren`
- Must Prepare Spells: `No`
- Can Learn Spells: `No`
- Base HP: `10`
- HP Per Level: `6`
- Common/Class/Items Hotbar Columns: `9 / 5 / 2`
- 主职业 `IsMulticlass = No`
- 多职业入口 `IsMulticlass = Yes`
- 两条 ClassDescriptions UUID 必须不同
- 两条记录都指向主职业 Progression Table

## 3. L1–L12 Progression 不变量

所有 `QTD_GreatSage_1` 到 `QTD_GreatSage_12`：

- `ProgressionType = 0`
- 共享同一个 TableUUID
- 每行 UUID 唯一
- `AllowImprovement = Yes` 只允许出现在 L4 / L8 / L12

关键等级：

| Level | 必须出现 |
|---|---|
| L1 | `QTD_SageQi +2`，灵猴身法，如意兵法 |
| L2 | `QTD_SageQi +1`，铜头铁臂，L2 SpellList |
| L3 | 七十二变入口，L3 SpellList，三个子职业 |
| L4 | Feat |
| L5 | `QTD_SageQi +1`，Extra Attack，苍鹰/猛虎变化 |
| L6 | L6 SpellList：火眼金睛 + 身外身法 |
| L7 | 大圣闪避 |
| L8 | Feat，`QTD_SageQi +1` |
| L9 | 金刚不坏 |
| L10 | 三头六臂 |
| L11 | `QTD_SageQi +1`，当前 forward trunk 还接入法天象地预览 |
| L12 | Feat，齐天大圣封顶被动；被动额外增加 `QTD_SageQi +2` |

## 4. 仙力曲线

基础主职业 Progression 累计：

- L1 = 2
- L2 = 3
- L5 = 4
- L8 = 5
- L11 = 6

L12 的 `QTD_Passive_QitianDasheng` 再增加 2，当前 trunk 预期总上限为 8。

`QTD_SageQi` 必须：

- 显示在 Action Resource 面板
- Short Rest 全恢复
- Long Rest 后同样处于满值
- 0 点时所有需要仙力的技能不可施放
- Respec 后不残留旧上限
- Multiclass 下只按实际 `QTD_GreatSage` 等级获得对应资源增量

## 5. SpellList 绑定

当前 canonical Tech Name：

- L2 `QTD_SpellList_L2` → `Target_QTD_SomersaultCloud`
- L3 `QTD_SpellList_L3` → `Zone_QTD_SeaCalmingStrike`
- L6 `QTD_SpellList_L6` → `Target_QTD_FieryGoldenEyes;Target_QTD_HairClones`

不要再使用旧的 Shout 版本名称。

## 6. Toolkit 实际 UUID 回填

每创建一个对象，就在 `data/toolkit_spine_recording.csv` 填：

- `ToolkitUUID`
- `LocalState`
- `Notes`

推荐状态：

- `pending-toolkit-entry`
- `entered-not-tested`
- `basic-level-a-pass`
- `combat-pass`
- `toolkit-verified`

只有对象已在本机 Toolkit 创建、`Basic_Level_A` 通过、无 Stats/UUID 错误，并完成至少一次相关实测后，才允许写 `toolkit-verified`。

## 7. Basic_Level_A 验收顺序

1. Character Creation 能看到齐天大圣。
2. 主职业初始 HP/属性提示/Hotbar 正常。
3. 仙力 L1 = 2。
4. `Ctrl+Shift+L` 逐级升到 L12。
5. 每一级都能完成，不出现空白奖励页。
6. L3 同时出现三个子职业。
7. L4/L8/L12 出现 Feat。
8. L5 Extra Attack 出现。
9. 仙力依次达到 2/3/4/5/6，L12 forward trunk 为 8。
10. Short Rest 恢复仙力。
11. Respec 后重新走一遍 L1–L12。
12. 测一次 Multiclass，确认资源按大圣职业等级而不是总角色等级成长。

## 8. 当前完成定义

这一阶段完成不代表 V0.1 整体发布完成。它只代表职业“脊柱”成立：

- ClassDescriptions 可加载
- Progressions 可升级
- Sage Qi 可消耗/恢复
- SpellList/Feat/Subclass 入口按等级出现
- Toolkit 实际 UUID 已回填

之后再进入 V0.1 三基础被动、三核心技能和三件装备的运行时收口。