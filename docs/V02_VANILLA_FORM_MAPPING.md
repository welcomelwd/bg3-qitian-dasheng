# V0.2 原版形态映射

本文件用于把“七十二变”的首批三个原型映射到已经存在、经过游戏验证的 BG3 变身形态。目标是先复用稳定的变身链路，再逐步替换视觉、技能和数值，而不是从空白 POLYMORPHED 状态开始造轮子。

## 总体原则

1. 所有 QTD 形态使用独立 `QTD_Transform_*` Spell / Status / RootTemplate 条目，不覆盖 Vanilla Wild Shape。
2. 变身 Status 必须保持与原版兽形兼容的 `POLYMORPHED` 路线，并在 Toolkit 中确认 `SG_Polymorph_BeastShape` 等 StatusGroup。
3. 首轮只克隆稳定行为，不复制第三方 MOD 的资产或源码。
4. 模型与技能可以二阶段替换。第一阶段优先验证：进入、退出、0 HP 恢复、装备恢复、热栏、移动和战斗。

## 1. 小虫变化 → Cat 技术模板

**QTD 条目**：`QTD_Transform_Insect`

**第一阶段参考**：Vanilla Wild Shape: Cat。

原因：
- Cat 是最适合验证 Tiny 体型、探索、潜行、交互的稳定兽形之一。
- 官方 Toolkit 文档可确认 `Skill_Druid_WildShape_Cat` 图标 TechName，说明 Cat Wild Shape 资源可直接在 Toolkit 中检索。
- Druid Quality of Life 的 Patch 8 版本继续以 Cat Wild Shape 做互动/潜行能力扩展，说明这条形态链路适合探索型原型。

第一阶段保留：
- Tiny 体型与基础移动/交互链路。
- Dismiss / revert 行为。
- 变身状态与装备恢复行为。

第一阶段移除/替换：
- `Meow` 等猫专属表现。
- 猫图标和文字。

第二阶段：
- 在 Root Template Manager 里寻找可用的虫类/小动物 NPC RootTemplate。
- 只有当目标模型的移动、互动、死亡和变身动画稳定时，再替换 Cat RootTemplate。

## 2. 苍鹰变化 → Dire Raven 引擎模板

**QTD 条目**：`QTD_Transform_Eagle`

**第一阶段参考**：Vanilla Wild Shape: Dire Raven。

原因：
- Dire Raven 已具备 Wild Shape + Fly + Dismiss 的完整飞行形态链路。
- 多个成熟 Wild Shape MOD 都围绕 Dire Raven 修改飞行、攻击与能力，说明它是稳定的飞行基线。
- Giant Eagle 在多个 MOD 中被新增为 Wild Shape，但并非我们要依赖的基础前提。因此首版用 Dire Raven 验证引擎行为更稳。

第一阶段保留：
- Fly / flying movement。
- 空中寻路与落点逻辑。
- Wild Shape 进入/退出链路。

第一阶段替换：
- Raven 的 Beak / Rend Vision 后续替换为 `QTD_Eagle_Talon`、`QTD_Eagle_Dive`。
- 显示名、图标、说明全部使用苍鹰主题。

第二阶段：
- 在 Root Templates 中验证 Giant Eagle 模型是否能安全作为 polymorph RootTemplate。
- 若稳定，再把视觉从 Dire Raven 升级到 Giant Eagle，而不改变 QTD Spell/Status TechName。

## 3. 猛虎变化 → Sabre-Toothed Tiger 模板

**QTD 条目**：`QTD_Transform_Tiger`

**第一阶段参考**：Vanilla Wild Shape: Sabre-Toothed Tiger。

原因：
- 它本身就是成熟的近战大型猫科 Wild Shape。
- Druid Wild Shape Overhaul、Druid Wildshape Viability、Circle of the Claw 等作者都把 Saber-Toothed Tiger 作为近战/耐久输出形态继续扩展。
- 它非常适合验证 transformed HP、近战攻击、Pounce、0 HP 恢复原形和装备恢复。

第一阶段保留：
- 大型猫科 RootTemplate / locomotion。
- Bite/Claw 一类基础近战动画。
- 原版 Wild Shape revert 链路。

QTD 调整：
- 2 Sage Qi。
- 保留一套基础近战攻击，删掉不符合孙悟空变化定位的冗余能力。
- 后续添加 `QTD_Tiger_Pounce` 和咆哮控制技能。

## Toolkit 查找顺序

对每个原型执行：

1. Stats Editor 中搜索对应 Wild Shape SpellData。
2. 找到其应用的 POLYMORPHED StatusData。
3. 记录 Status 的 StatusGroup、StackId、Boosts、RootTemplate、OnRemove/OnApply 相关字段。
4. 在 Root Template Manager 打开对应 creature template。
5. 新建 QTD 独立副本，并替换所有互相引用为 QTD TechName/UUID。
6. 不修改 Shared / GustavDev 原条目。
7. 在 `Basic_Level_A` 逐个验证。

## 第一轮验收矩阵

| 原型 | 关键验证 | 成功标准 |
|---|---|---|
| 小虫 | Tiny / 探索 | 能进入、移动、通过窄小区域、手动退出，装备恢复 |
| 苍鹰 | Fly | 能飞到高低差位置、正常落地、退出后位置/装备正常 |
| 猛虎 | Combat HP | 能攻击、受伤、0 HP 恢复原形、原角色不直接死亡 |

## 兼容性重点

第三方 MOD 的实践显示：对 Wild Shape 直接覆盖原条目很容易和其他 Druid/Wild Shape MOD 冲突。QTD 因此坚持独立 Spell + Status + Container + Unlock Passive，不覆写 Vanilla Wild Shape 列表和状态。
