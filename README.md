# 齐天大圣 / Qitian Dasheng — BG3 Mod

一个以《西游记》孙悟空为核心主题的《博德之门 3》职业与装备模组工程。

> 当前阶段：**V0.1 Stats 实现草案 / Toolkit 模板克隆阶段**  
> 目标：先完成可创建、可升级、可战斗、可测试的独立职业，再扩展七十二变、毫毛分身与法天象地。

## V0.1 范围

- 独立职业：**齐天大圣 / Great Sage**
- 独立职业资源：**仙力 / Sage Qi**
- 核心被动：灵猴身法、如意兵法、铜头铁臂
- 核心技能：筋斗云、定海一棒、火眼金睛
- 代表装备：如意金箍棒、锁子黄金甲、藕丝步云履
- 1–12 级 Progression 骨架
- Toolkit 测试与验收清单

## 技术路线

V0.1 优先使用 **Baldur's Gate 3 Toolkit 原生能力**，不把 Script Extender 作为硬依赖。复杂的七十二变、毫毛分身和特殊事件逻辑在后续版本评估 BG3 Script Extender。

> `data/` 是设计与录入的 source-of-truth。`src/stats/` 是实现导向的 Stats 草案。`toolkit/` 用于保存 Toolkit 实际导出/生成的数据。不要把未经 Toolkit 验证的手写 Stats/LSX 当作已可运行资产。

## 项目结构

```text
bg3-qitian-dasheng/
├── data/                       # 结构化设计数据、UUID、等级表
├── docs/                       # 设计、Toolkit 实施、Clone Matrix、测试与路线图
├── src/stats/                  # 实现导向 Stats 草案
├── scripts/                    # 规格与 Stats 草案校验脚本
├── toolkit/                    # BG3 Toolkit 工程导出目录骨架
├── .github/ISSUE_TEMPLATE/     # Bug / 功能模板
├── CHANGELOG.md
└── README.md
```

## 关键 Tech Name

| 类型 | Tech Name |
|---|---|
| Class | `QTD_GreatSage` |
| Resource | `QTD_SageQi` |
| Passive | `QTD_Passive_MonkeyAgility` |
| Passive | `QTD_Passive_RuyiMastery` |
| Spell | `Target_QTD_SomersaultCloud` |
| Spell | `Zone_QTD_SeaCalmingStrike` |
| Spell | `Target_QTD_FieryGoldenEyes` |
| Weapon | `WPN_QTD_RuyiJinguBang` |

## 当前已对齐的原版模式

- 筋斗云：以 `Target_MistyStep` 作为可选落点传送的行为参考。
- 筋斗云核心位移：使用官方文档确认的 `TeleportSource()` Functor。
- 定海一棒：使用官方文档确认的 Strength Saving Throw、`DealDamage()`、`ApplyStatus()` 与 `Force()` 模式。
- 起始装备：采用官方 ClassDescriptions → ClassEquipment → Equipment 表流程。

仍需本机 Toolkit 验证的 Parent、动画、VFX、武器伤害与条件逻辑，请看 `docs/TOOLKIT_CLONE_MATRIX.md`。

## 开始开发

1. 安装 BG3 Toolkit，并新建 `QitianDasheng` Mod。
2. 按 `docs/TOOLKIT_IMPLEMENTATION.md` 创建 Progressions、ClassDescriptions 与资源。
3. 按 `docs/TOOLKIT_CLONE_MATRIX.md` 在 Shared/GustavDev 中查找并克隆原版参考记录。
4. 将 Toolkit 自动生成的 UUID 与 `data/uuid_manifest.json` 对齐。若 Toolkit 已生成 UUID，以 Toolkit 为准并更新 manifest。
5. 按 `data/progressions.csv` 录入 1–12 级成长。
6. 完成每个技能/被动后，在 `data/implementation_status.csv` 更新状态。
7. 在 `Basic_Level_A` 进行快速升级测试，再在正式存档新建角色回归测试。

## 设计原则

- **猴味优先**：机动、棒术、变化、洞察是体验核心。
- **强但不无脑**：V0.1 先对齐 BG3 原版高强度职业的战斗节奏。
- **渐进实现**：玩法先于自定义 3D 模型。
- **可维护**：内部名称统一 `QTD_` 前缀，所有关键对象均有 UUID 清单。
- **不猜内部 ID**：能从官方文档确认的先落地，不能确认的必须在 Toolkit 中克隆/验证。

## 免责声明

本项目为非官方粉丝模组工程，与 Larian Studios、Wizards of the Coast 或《西游记》相关权利方不存在官方隶属关系。请遵守游戏、Toolkit 与发布平台的相关条款。
