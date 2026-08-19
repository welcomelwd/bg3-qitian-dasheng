# Roadmap

## 当前整合门禁
- 暂停继续增加基础职业/子职业核心机制，优先关闭 `data/runtime_validation_matrix.csv` 中的 P0。
- P0 顺序：职业/仙力 → V0.1 核心被动与装备 Parent → 核心技能 → 七十二变恢复链 → 四档分身 RootTemplate。
- P1 再做三个子职业、L7/L9 防御、三头六臂的组合回归。
- `main` 当前是前向 trunk，已经包含 V0.4/V1.0 规划能力；V0.3 打包前必须确定 preview trunk 或真正 release slicing。
- 详见 `docs/V01_V03_INTEGRATION_AUDIT.md`。

## V0.1 — 大圣初现
- 独立职业
- 仙力
- 灵猴身法 / 如意兵法 / 铜头铁臂
- 筋斗云 / 定海一棒 / 火眼金睛
- 金箍棒 / 黄金甲 / 步云履
- 完成 Toolkit Parent / SpellData 克隆验证
- 完成 Basic_Level_A 与实际战斗测试

## V0.2 — 七十二变
- 大圣闪避、金刚不坏
- 七十二变主容器 `QTD_TransformContainer`
- 使用独立 `QTD_Transform_*` 条目，不覆盖 vanilla Wild Shape
- 使用隐藏 Unlock Passive 按等级开放形态
- 统一使用 Sage Qi：工具形态 1 / 战斗形态 2 / 高级形态 3
- 第一批原型：苍鹰、猛虎、小虫
- 验证 0 HP 恢复原形、装备与状态恢复
- 毫毛分身原型

## V0.3 — 大闹天宫
- `QTD_VictoriousBuddha` 斗战胜佛：L3/L6/L10 已接入
- `QTD_SeventyTwoChanges` 七十二变：L3 蜘蛛、L6 黑豹、L10 枭熊/双脊龙已接入
- `QTD_SpiritualStoneMonkey` 灵明石猴：L3 灵台悟法/三昧真火、L6 风雷云遁/掌心雷、L10 五行仙法已接入
- 三个子职业均使用独立 Progression Table，并在主职业 L3 同时开放
- 三头六臂
- V0.3 发布前先通过整合审计 P0/P1 门禁
- P0/P1 通过后再继续武器专属 VFX、筋斗云落点 VFX / Cloud Momentum 视觉抛光
- 扩展巨猿、石像、妖王等高阶视觉变化放入后续非阻塞阶段

## V0.4 — 法天象地
- 法天象地
- 四件套联动
- 自定义 3D 武器/装备资源
- 评估自定义变化模型

## V1.0 — 西游完整体验
- L12 `QTD_Passive_QitianDasheng` 齐天大圣封顶被动
- 仙力上限从 6 提升至 8、常驻移动 +3m、免疫魅惑与恐惧
- L12 不新增额外 Action / Bonus Action / 更高 Extra Attack 链
- 完整汉化/英文本地化
- 音效/VFX/图标统一
- 获取任务与彩蛋物品
- 兼容性与平衡回归
- 发布包与安装文档
