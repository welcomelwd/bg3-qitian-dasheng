# 齐天大圣 / Qitian Dasheng — BG3 Mod

一个以《西游记》孙悟空为核心主题的《博德之门 3》职业与装备模组工程。

> 当前阶段：**基础职业 L1–L12 Stats/规格链已贯通，进入 Patch 8 Toolkit 实机验证与内容扩展阶段。**  
> 当前重点：验证 Parent/RootTemplate、变身、分身、三头六臂、法天象地、L12 封顶被动，以及装备/动画/VFX 的实际运行表现。

## 当前基础职业主干

- 独立职业：**齐天大圣 / Great Sage**
- 独立职业资源：**仙力 / Sage Qi**
- L1：灵猴身法、如意兵法
- L2：铜头铁臂、筋斗云
- L3：七十二变、小虫变化、定海一棒
- L5：额外攻击、苍鹰变化、猛虎变化
- L6：火眼金睛、身外身法
- L7：大圣闪避
- L9：金刚不坏
- L10：三头六臂
- L11：法天象地
- L12：齐天大圣封顶被动 + Feat

L12 `QTD_Passive_QitianDasheng` 当前设计：仙力上限从 6 提升到 8、常驻移动 +3m、免疫魅惑与恐惧；不新增额外 Action / Bonus Action / 更高 Extra Attack 链。

## 代表装备

- 如意金箍棒 `WPN_QTD_RuyiJinguBang`
- 锁子黄金甲 `ARM_QTD_GoldenArmor`
- 藕丝步云履 `BOOTS_QTD_CloudWalking`
- 凤翅紫金冠：后续装备阶段加入

## 技术路线

基础实现优先使用 **Baldur's Gate 3 Toolkit 原生能力**，当前不把 Script Extender 作为硬依赖。若高级七十二变、分身复制、真正 Huge 法天象地碰撞体等机制在 Toolkit 原生路径下无法稳定实现，再单独评估 BG3 Script Extender。

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
| Transform Container | `QTD_TransformContainer` |
| Spell | `Target_QTD_SomersaultCloud` |
| Spell | `Zone_QTD_SeaCalmingStrike` |
| Spell | `Target_QTD_FieryGoldenEyes` |
| Spell | `Target_QTD_HairClones` |
| Spell | `Shout_QTD_ThreeHeadsSixArms` |
| Spell | `Shout_QTD_FaTianXiangDi` |
| Passive | `QTD_Passive_QitianDasheng` |
| Weapon | `WPN_QTD_RuyiJinguBang` |

## 当前已对齐的实现模式

- 筋斗云：`Target_MistyStep` + `TeleportSource()`。
- 定海一棒：Strength Saving Throw + `DealDamage()` + `ApplyStatus()` + `Force()`。
- 七十二变：独立 `QTD_Transform_*` + linked container + unlock passives，不覆盖 vanilla Wild Shape。
- 身外身法：固定分身模板分级成长，保持两具分身与三回合寿命。
- 三头六臂：三回合 BOOST 形态，使用 `ExtraAttack_2`，不复制真实武器槽。
- 法天象地：Enlarge 同源 `ObjectSize(+1)` / `ScaleMultiplier(1.33)`，STR 最低 25，附带三种专属战技。
- 齐天大圣：PassiveData `ActionResource(...)` + `MovementSpeed(...)` + 状态组免疫。
- 起始装备：ClassDescriptions → ClassEquipment → Equipment 表流程。

仍需本机 Toolkit 验证的 Parent、RootTemplate、动画、VFX、碰撞、变身恢复和武器条件逻辑，请看 `docs/TOOLKIT_CLONE_MATRIX.md` 与各专项设计文档。

## 开始开发 / 实机验证

1. 安装 BG3 Toolkit，并打开/创建 `QitianDasheng` Mod。
2. 按 `docs/TOOLKIT_IMPLEMENTATION.md` 创建 Progressions、ClassDescriptions 与资源。
3. 按 `docs/TOOLKIT_CLONE_MATRIX.md` 在 Shared/GustavDev 中查找并克隆原版参考记录。
4. 将 Toolkit 自动生成的 UUID 与 `data/uuid_manifest.json` 对齐。若 Toolkit 已生成 UUID，以 Toolkit 为准并更新 manifest。
5. 按 `data/progressions.csv` 录入并核对 1–12 级成长。
6. 按 `data/implementation_status.csv` 和 GitHub Issues 逐项完成验证门。
7. 在 `Basic_Level_A` 做快速升级测试，再在正式战斗场景进行动作经济、状态恢复、变身与装备回归。

## 设计原则

- **猴味优先**：机动、棒术、变化、洞察是体验核心。
- **强但不无脑**：高等级强化避免无条件堆叠额外完整动作。
- **渐进实现**：玩法先于自定义 3D 模型。
- **可维护**：内部名称统一 `QTD_` 前缀，所有关键对象均有 UUID 清单。
- **不猜内部 ID**：能从文档/公开数据确认的先落地，不能确认的必须在 Toolkit 中克隆/验证。

## 免责声明

本项目为非官方粉丝模组工程，与 Larian Studios、Wizards of the Coast 或《西游记》相关权利方不存在官方隶属关系。请遵守游戏、Toolkit 与发布平台的相关条款。
