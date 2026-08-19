# V0.1 铜头铁臂运行时收口

目标：把 `QTD_Passive_CopperHeadIronArm` 从占位被动推进到 Patch 8 Toolkit 可直接验证的反应减伤链。

## 当前实现

### 可见被动

`QTD_Passive_CopperHeadIronArm`

- L2 解锁
- 显示 Reaction 消耗
- 解锁 `QTD_Interrupt_CopperHeadIronArm`

### 反应

`QTD_Interrupt_CopperHeadIronArm`

- `InterruptContext = OnPreDamage`
- `Container = YesNoDecision`
- `Cost = ReactionActionPoint:1`
- 只有攻击命中且主伤害类型为以下之一才允许弹出：
  - Bludgeoning
  - Piercing
  - Slashing
- `SG_Polymorph` 状态下禁用，避免动物/变化形态继续沿用本体铜头铁臂。

接受反应后，在当前受击者身上临时施加：

`QTD_STATUS_COPPER_HEAD_IRON_ARM_REDUCTION`

### 临时减伤状态

仅减少物理三类伤害：

- `DamageReduction(Bludgeoning, Flat, 1d8+WisdomModifier)`
- `DamageReduction(Piercing, Flat, 1d8+WisdomModifier)`
- `DamageReduction(Slashing, Flat, 1d8+WisdomModifier)`

不使用 `DamageReduction(All,...)`，因此目标是让武器附带的 Fire / Lightning / Force 等额外伤害保持原值。

状态带有隐藏 cleanup passive：

`QTD_Passive_CopperHeadIronArm_Cleanup`

在 `OnDamaged;OnDamagedPrevented` 后立即移除减伤状态，避免影响后续攻击。

## 数据模式依据

本实现组合了三类已经存在的 BG3 Stats 模式：

1. `OnPreDamage + YesNoDecision + ReactionActionPoint` 的反应链。
2. Uncanny Dodge 类实现使用 Interrupt 临时施加减伤状态，并在当前伤害结算后清理。
3. `DamageReduction(..., Flat, dice + ability modifier)` 支持骰子和属性修正表达式。

## Patch 8 Toolkit 验收

1. L2 能正常获得“铜头铁臂”。
2. 钝击攻击命中时弹出 Reaction 询问。
3. 穿刺攻击命中时弹出 Reaction 询问。
4. 挥砍攻击命中时弹出 Reaction 询问。
5. Fire / Cold / Lightning / Force / Psychic 等纯非物理攻击不应弹出。
6. 拒绝 Reaction 后不消耗 Reaction，也不降低伤害。
7. 接受 Reaction 后只消耗 1 次 Reaction。
8. 伤害降低值应为 `1d8 + WIS modifier`。
9. 同一攻击带元素附伤时，元素部分不得被该 B/P/S 状态削减。
10. 当减伤足以把当前物理伤害压到 0 时，cleanup 仍必须发生。
11. 连续两次受到攻击时，第二次若已经没有 Reaction 不应继续弹出或继续享受上一击减伤。
12. 一个攻击同时存在多种物理组件时，检查是否发生多次 1d8 独立结算；若发生，需进一步收窄实现。
13. 七十二变/其他 `SG_Polymorph` 状态下不应出现铜头铁臂 Reaction。
14. Save/Load、Respec、Multiclass 后重复测试，不能留下永久减伤状态。
15. 与 L9 金刚不坏组合测试，确认抗性与 Reaction 减伤的结算顺序可接受且不会重复无限减伤。

完成这些测试前，状态保持 `interrupt-pattern-aligned-draft`，不得标记为 `toolkit-verified`。
