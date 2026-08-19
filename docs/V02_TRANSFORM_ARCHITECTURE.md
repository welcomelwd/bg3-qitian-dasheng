# V0.2 七十二变技术架构

本方案根据公开的 Nexus 模组实现模式整理，目标是在不覆盖原版 Wild Shape 的前提下，为齐天大圣加入可扩展的多形态系统。

## 核心结构

```text
QTD_TransformContainer                # 玩家看到的主入口
├── QTD_Transform_Eagle               # 苍鹰
├── QTD_Transform_Tiger               # 猛虎
├── QTD_Transform_GiantApe            # 巨猿
├── QTD_Transform_Insect              # 小虫/潜行
├── QTD_Transform_Stone               # 石像/高防御
└── QTD_Transform_DemonKing           # 妖王/高级战斗形态
```

所有条目都必须是新的 `QTD_` 数据，不修改 vanilla Wild Shape SpellData、StatusData 或 Character 数据。

## 解锁方式

不要把全部形态直接塞进职业 Progression 的可见 SpellList。

使用隐藏 Passive 分批解锁：

```text
QTD_Passive_TransformUnlock_L3
QTD_Passive_TransformUnlock_L5
QTD_Passive_TransformUnlock_L7
QTD_Passive_TransformUnlock_L9
QTD_Passive_TransformUnlock_L11
```

建议：

- Level 3：灵猴 / 小虫
- Level 5：猛虎 / 苍鹰
- Level 7：石像
- Level 9：巨猿
- Level 11：妖王/高级形态

## 仙力成本

采用统一 Sage Qi，不新增 Wild Shape Charges：

| 类型 | Sage Qi |
|---|---:|
| 工具/潜入形态 | 1 |
| 常规战斗形态 | 2 |
| 大型/高级战斗形态 | 3 |

这样普通棒术、筋斗云和变化共享同一个资源经济。

## 形态规则

V0.2 原型至少验证：

1. 变身消耗正确仙力。
2. 0 HP 自动恢复原形。
3. 恢复原形后角色本体 HP/状态行为正常。
4. 装备在变身期间不会永久丢失。
5. 变身期间保留的悟空能力必须显式白名单，不默认全部继承。
6. 至少保留一个通用退出变身按钮。

### 保留能力白名单候选

第一阶段只考虑：

- 火眼金睛被动部分
- 特定高级形态的筋斗云/位移
- 大圣专用变身强化 Passive

不默认允许金箍棒攻击，因为多数动物形态没有正常持械骨骼与动画。

## 形态成长

参考成熟 Wild Shape 模组的思路，不为同一生物制作大量重复高阶 Spell。

形态通过等级 Passive 获得成长：

```text
QTD_Passive_FormScaling_L5
QTD_Passive_FormScaling_L8
QTD_Passive_FormScaling_L11
```

成长维度可包括：

- Temporary/Max HP
- AC
- Attack bonus
- Damage bonus
- 新形态能力

这能让早期形态在后期仍有功能价值。

## 第一批 Toolkit 原型

V0.2 不直接做全部形态。先做三个验证样本：

### A. 苍鹰
目的：验证飞行形态、移动能力和退出变身。

### B. 猛虎
目的：验证战斗形态、HP、攻击和资源成本。

### C. 小虫
目的：验证超小体型、探索/潜入用途。

三个样本稳定后，再扩展巨猿、石像和妖王。

## 与 Script Extender 的边界

V0.2 优先使用 Toolkit 原生 Wild Shape / Polymorph 体系。

仅在以下需求无法用原生数据稳定实现时考虑 BG3SE：

- 极复杂的本体/形态能力同步
- 动态形态列表
- 高级毫毛分身 AI/生命周期
- 非标准模型动态替换

因此七十二变本身不自动成为 BG3SE 硬依赖。
