# Nexus Mods Reference Research

> 目的：研究公开的 BG3 模组设计/实现模式，为齐天大圣模组提供结构参考。除非作者许可明确允许，否则不复制其他作者的源码、模型、图标、VFX 或打包文件；本文件只记录公开页面中可观察到的架构与玩法模式。

## 参考样本

### 1. Soulshifter Class and Specter Subclass
- Nexus: https://www.nexusmods.com/baldursgate3/mods/11534
- 价值：与齐天大圣最接近的“独立职业 + 自定义资源 + 多形态变身”样本。
- 公开页面显示：
  - 使用自定义资源 `Soul Points`。
  - 1 级 2 点，后续等级继续增加资源。
  - 不同变身形态可以消耗不同数量的 Soul Points。
  - 变身后替换能力，0 HP 时恢复原形。
  - 形态按等级逐步解锁。
- 对 QitianDasheng 的启发：
  - `QTD_SageQi` 同时作为普通神通和变身资源是可行的。
  - 七十二变应采用“弱形态 1 点 / 战斗形态 2 点 / 高级形态 3 点”的成本层级。
  - 形态不要在 3 级一次塞完，应该随等级逐步解锁。
  - 变身应定义清晰的恢复原形、HP、能力继承规则。

### 2. Cloudshift
- Nexus: https://www.nexusmods.com/baldursgate3/mods/18920
- 价值：Misty Step 风格自定义瞬移的直接对照样本。
- 公开页面显示作者分别实现了 Teleportation Spell 与 Target Spell 两类版本：
  - Teleportation 版本需要先选自己再选落点，可在起点和终点触发效果。
  - Target 版本直接选择落点，效果集中在落点。
  - Target 版本仍可保持类似 Vanilla Misty Step 的交互。
- 对 QitianDasheng 的启发：
  - `Target_QTD_SomersaultCloud` 的路线是合理的，避免多一步“选自己”。
  - V0.1 先保持纯落点传送；后续可在抵达点增加云爆/雷鸣/冲势，而无需改成 Teleportation 类型。

### 3. Druid Wild Shape Overhaul
- Nexus: https://www.nexusmods.com/baldursgate3/mods/1148
- 价值：成熟的大型多形态系统和兼容性样本。
- 公开页面明确说明：
  - Wild Shape 技能从原 spell list 中移除，改为通过 unlock passives 发放。
  - 所有形态和 spell container 使用新的独立条目，而不是直接修改 vanilla Wild Shape 条目。
  - 这种做法用来隔离其他 Wild Shape 模组对自身数据的影响。
  - 形态按等级继续增加能力与强度，而不是每个形态完全静态。
- 对 QitianDasheng 的启发：
  - 七十二变使用独立 `QTD_Transform_*` 条目，不覆盖任何 vanilla Wild Shape。
  - 用隐藏/解锁 Passive 控制各等级可用形态，避免 Level Up 页面被大量变身 spell 塞满。
  - 每个形态应允许后续等级强化，而不是制作大量重复“高级版形态”。

### 4. Sunscream - Custom Wild Shape Tutorial
- Nexus: https://www.nexusmods.com/baldursgate3/mods/15724
- 价值：专门针对 BG3 Toolkit 的自定义 Wild Shape 教学样本。
- 页面说明该文件就是作者 Toolkit 自定义 Wild Shape 教程配套模组。
- 对 QitianDasheng 的启发：
  - V0.2 优先在 Toolkit 原生变身链路上实现，不提前把 BG3SE 设为硬依赖。
  - 第一批形态应先选复用游戏现成骨骼/模型的动物或怪物，验证状态转换和能力继承，再考虑自定义模型。

### 5. Polymath - Automated Mod Making
- Nexus: https://www.nexusmods.com/baldursgate3/mods/6318
- 价值：数据结构与 Patch 8 数据参考工具。
- 作者公开说明 Polymath 支持：自定义 class/subclass、spell/action resource、passive、weapon/armor，并可导出游戏已有 spell 供修改；作者还提供了 Patch 8 各 PAK 的数据表用于 Toolkit 参考。
- 注意：作者说明 source available，但不是 open source；因此只把它当数据/工作流参考，不复制其源码。
- 对 QitianDasheng 的启发：
  - 后续可用 Polymath 的 Patch 8 数据表辅助筛选 Parent/SpellData，而实际结果仍以 Toolkit 中的 Shared/GustavDev 数据为准。

### 6. Truly Legendary - Blood Of Lathander
- Nexus: https://www.nexusmods.com/baldursgate3/mods/14596
- 价值：传奇武器数值与 STR/DEX 双路线参考。
- 页面公开说明其通过 Finesse 让武器使用 Strength / Dexterity 中更高的 Modifier。
- 对 QitianDasheng 的启发：
  - V0.1 的 `Ruyi Mastery` 不必自己发明“max(STR,DEX)”攻击公式，可以优先验证给金箍棒加入 Finesse 是否已经满足双路线需求。
  - 将该逻辑限定在金箍棒/指定棍类上，比全职业修改攻击属性更安全。

## 当前采用的设计决策

1. **筋斗云**：保持 `Target_QTD_SomersaultCloud`，行为基线为 Misty Step / Cloudshift Target 模式。
2. **七十二变**：独立新条目，不修改 vanilla Wild Shape。
3. **变身发放**：优先使用 unlock passives + 一个主变身容器，而不是让所有形态直接出现在升级 UI。
4. **资源成本**：弱形态 1 Sage Qi，标准战斗形态 2，高级/大型形态 3。
5. **资源恢复**：V0.2 继续沿用 Sage Qi 的短休恢复设计，避免再引入第二种变身资源。
6. **如意兵法**：优先验证 Finesse/武器属性机制，避免自造高风险攻击公式。
7. **知识产权边界**：Nexus 样本用于结构研究；任何作者限制修改/资产复用的文件不导入仓库。
