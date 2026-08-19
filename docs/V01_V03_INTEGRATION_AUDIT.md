# V0.1–V0.3 全职业整合审计

审计快照：2026-08-19  
基线提交：`8ef23d480d370d28987e73217867ecef27e22fa0`

## 结论

当前工程已经完成齐天大圣 L1–L12 主职业骨架和三个 L3/L6/L10 子职业的数据接线，但**还不能称为 Patch 8 runtime-ready**。下一阶段暂停继续增加核心技能，优先关闭 `data/runtime_validation_matrix.csv` 中的 P0 门禁。

当前最重要的发布阻塞点集中在：

1. `QTD_GreatSage` / `QTD_SageQi` 的 Toolkit 实际对象、UUID、恢复行为和 1–12 级升级链。
2. V0.1 三个基础被动仍有机制缺口：灵猴身法的未着甲 AC/坠落减伤、如意兵法的 STR/DEX 选择、铜头铁臂的 Reaction 减伤。
3. V0.1 三个核心技能仍有 Toolkit Gate：筋斗云云势与等级距离、定海一棒武器伤害/几何、火眼金睛反隐身/AC/攻击者限定优势。
4. 金箍棒、黄金甲、步云履仍保留 Parent 占位，起始装备只能在实际 Toolkit 对象创建后闭环。
5. 七十二变必须验证 0 HP 恢复、手动退出、装备/Hotbar 恢复和多人容器隔离。
6. 身外身法的四档 Character RootTemplate 与共享武器 RootTemplate 仍未落入真实 Toolkit 导出。
7. `main` 是**前向 trunk**：L11 已接入目标版本 V0.4 的法天象地，L12 已接入目标版本 V1.0 的齐天大圣封顶。V0.3 打包前必须明确是发布 preview trunk，还是对未来能力做真正的 release slicing。

## 资源曲线

基础仙力上限按主职业成长：

| 等级 | 累计仙力 |
|---|---:|
| L1 | 2 |
| L2 | 3 |
| L5 | 4 |
| L8 | 5 |
| L11 | 6 |
| L12 | 8（齐天大圣 +2） |

高等级资源压力需要实机回归：

- L10 三头六臂消耗 4 / 5，正常施放后只剩 1 点。
- L11 法天象地消耗 5 / 6，正常施放后只剩 1 点。
- L12 法天象地 5 + 任一 3 仙力高阶仙术可以吃完整个 8 点池。如果 Haste / Action Surge 允许同回合完成组合，必须确认没有资源恢复、免费施法或异常 Action 链。

## 动作经济审计

规格层没有发现故意设计的无限 Action 链：

- 三头六臂通过 `ExtraAttack_2` 升级 Attack Action 内的武器攻击次数，不授予完整 ActionPoint。
- 法天象地启动自身消耗 Action，并显式禁止额外 ActionPoint / ExtraAttack_2。
- L12 齐天大圣只增加仙力上限、移动和心智免疫，不增加 Action / Bonus Action / 更高 Extra Attack。
- 三个子职业均不改变基础 Action 容量；灵明石猴也不获得 SpellSlot。

仍需组合验证：Three Heads Six Arms + Haste / Action Surge、Fa Tian Xiang Di + Haste / Action Surge、不同子职业技能与基础 Extra Attack 的组合。

## P0：可玩版发布阻塞

### P0-1 职业与资源

- 在 Toolkit 创建/确认 `QTD_GreatSage` 主职业、多职业入口和三个子职业 ClassDescriptions。
- 创建真实 `QTD_SageQi` ActionResourceDefinitions，确认 Short Rest 全恢复。
- 录入并验证 1–12 级 Progressions、4/8/12 Feat 和 L3 三子职业选择。
- `Basic_Level_A` 从 L1 快速升到 L12，不允许空白升级页、崩溃或 UUID/Stats 报错。

### P0-2 V0.1 基础被动

- `QTD_Passive_MonkeyAgility`：补齐未着甲 AC = 10 + DEX + WIS 与坠落伤害处理。
- `QTD_Passive_RuyiMastery`：找到可靠的 Quarterstaff/Ruyi STR/DEX 选择条件。
- `QTD_Passive_CopperHeadIronArm`：从原版 Reaction 模式克隆可验证的物理减伤链。

### P0-3 V0.1 核心技能

- 筋斗云：12/15/18/21m 等级成长 + `QTD_STATUS_CLOUD_MOMENTUM` 的施法者状态时序。
- 定海一棒：主手武器伤害组件 + 雷鸣成长 + 正确 Zone 几何。
- 火眼金睛：显形/反隐形、AC -2 与仅悟空受益的攻击优势。

### P0-4 装备

- 用真实 Quarterstaff Parent 替换 `TODO_TOOLKIT_CLONE_QUARTERSTAFF_TEMPLATE`。
- 用真实 Armor/Boots Parent 替换两个装备占位。
- 创建 RootTemplate / Equipment 表，并验证 Character Creation 初始装备。
- 如意伸长先保证真实武器命中，再考虑 Reach/VFX。

### P0-5 七十二变基础链

优先测试小虫、苍鹰、猛虎：手动退出、0 HP 恢复、装备恢复、Hotbar 恢复、状态清理、飞行/路径、多人不污染共享容器。

`data/transforms.yaml` 中 L7/L9/L11 unlock passive 和 L5/L8/L11 scaling passive 仍属于未来占位，不应视为已经实现。

### P0-6 身外身法 RootTemplate

建立并验证 L6/L8/L10/L12 四档 `QTD_HairClone_Root_*` 和 `QTD_HairCloneStaff_Root`。两只分身必须稳定出现、3 回合消失、重施替换旧分身，不能掉落/复制唯一装备。

### P0-7 发布切片

在 V0.3 tag/PAK 前二选一：

- **preview trunk**：明确声明测试包包含已经接入 progression 的 V0.4/V1.0 预览能力；或
- **release slicing**：V0.3 发布构建排除 L11 法天象地与 L12 封顶的未来版本接线，`main` 继续保留前向开发状态。

不做这个决策，就无法准确描述 V0.3 的真实内容边界。

## P1：组合与子职业回归

1. L7 大圣闪避 / L9 金刚不坏的实际伤害、豁免、与铜头铁臂叠加。
2. L10 三头六臂：恰好三次武器攻击，重点测 Haste、Action Surge、变身、分身。
3. 斗战胜佛：L3 暴击骰、19–20 暴击、`AC(-2)`、未来武器限制。
4. 七十二变子职业：蜘蛛、黑豹、枭熊、双脊龙 helper status 与退出清理。
5. 灵明石猴：传送后的 `SELF` Momentum、五行容器只出现 5 个 QTD child、不泄漏 Ki/SpellSlot。
6. Respec、Multiclass、Save/Load、Short/Long Rest、双人/多人齐天大圣。

## P2：后续版本与视觉

- 法天象地真正巨大碰撞、9m 擎天一柱、相机和 VFX。
- L12 封顶资源/Respec 回归。
- 三头六臂额外手臂/头部幻影 VFX。
- 金箍棒、黄金甲、步云履和未来凤翅紫金冠的自定义视觉。
- 巨猿、石像、妖王等未来变化。
- 清理 `transforms.yaml` 中未接线的未来 unlock/scaling 占位，或在真正实现时升级其状态。

## 推荐 Toolkit 测试顺序

0. ActionResourceDefinitions + ClassDescriptions + Progressions + Equipment。
1. Character Creation、L1–L12 升级、Feat、仙力上限/恢复。
2. V0.1 三基础被动、三核心技能、三件装备。
3. 基础七十二变 Cat/Raven/Sabre-Tooth 恢复链。
4. 身外身法四档 RootTemplate + 共享毫毛棍。
5. L7/L9 防御。
6. 分别创建三名角色测试三个子职业 L3/L6/L10。
7. 三头六臂 + Haste / Action Surge / 变身 / 分身组合。
8. Respec / Multiclass / Save-Load / Multiplayer 回归。
9. 最后再验证 V0.4 法天象地与 V1.0 封顶。

## V0.3 可玩版完成定义

V0.3 可以进入可玩测试包前至少满足：

- `runtime_validation_matrix.csv` 所有 P0 已关闭。
- 所有 P1 至少有一次 `Basic_Level_A` + 正式战斗记录，且无 crash、soft-lock 或永久数据污染。
- 灵明石猴没有 Ki/SpellSlot 泄漏。
- 七十二变没有覆盖 vanilla Wild Shape 条目。
- 分身不留下永久角色/装备/状态。
- Respec 与多人模式不会污染子职业、容器和状态。
- 明确 V0.3 的 release scope。

只有经过本机 Patch 8 Toolkit 验证并实际战斗通过的对象，才能升级为 `toolkit-verified`。