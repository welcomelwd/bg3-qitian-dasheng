# V0.1 火眼金睛 / Fiery Golden Eyes

## 目标

`Target_QTD_FieryGoldenEyes` 是 L6 基础职业技能：

- Bonus Action ×1
- QTD_SageQi ×1
- 18m
- 目标获得 `QTD_STATUS_DEMON_REVEALED`，持续 3 回合
- 施加时移除 `SG_Invisible`
- 持续期间通过 `StatusImmunity(SG_Invisible)` 阻止再次进入普通隐形组
- 目标 AC -2
- 只有施加该状态的 Great Sage 对该目标攻击获得 Advantage

## 来源绑定优势

L6 同时获得隐藏被动：

`QTD_Passive_FieryGoldenEyes_TargetAdvantage`

使用：

```txt
IF(HasStatus('QTD_STATUS_DEMON_REVEALED',context.Target,context.Source)):Advantage(AttackRoll)
```

三参数 `HasStatus(status,target,source)` 用来绑定状态来源。设计目标是：A 大圣标记目标后，A 获得 Advantage；B 大圣不会因为 A 的标记自动获得 Advantage。

## 隐形处理

目标状态：

```txt
OnApplyFunctors "RemoveStatus(SG_Invisible)"
Boosts "AC(-2);StatusImmunity(SG_Invisible)"
```

这样把“立即揭露”和“持续阻止再隐形”拆成两个动作。

## 项目所有者实机验证清单

1. 对已经处于 `INVISIBLE` / `INVISIBILITY` 的目标施放，目标立即显形。
2. 显形持续 3 回合。
3. 持续期间普通隐形技能/药水不能重新获得 `SG_Invisible`。
4. AC 精确降低 2。
5. 施术者攻击自己标记的目标获得 Advantage。
6. 另一名 Great Sage 攻击该目标不应自动获得 Advantage。
7. 普通队友攻击该目标不应因为火眼金睛本身自动获得 Advantage。
8. A 标记后 B 再次标记同一目标时，检查 StackId / source ownership 是否切换到 B；若引擎保留旧 source，需要改为更明确的 owner helper 链。
9. Save/Load 后 source ownership 不应丢失。
10. Respec 后隐藏攻击被动应正确移除/恢复。
11. 七十二变状态下是否允许施放按最终设计确认，目前未主动增加额外变身限制。
12. 对特殊剧情隐形、脚本隐形或不属于 `SG_Invisible` 的效果单独记录，不强行扩大 V0.1 的状态组范围。

## 延后项

“对妖邪额外 +1d6 Radiant”暂不进入 V0.1。原因是需要先定义稳定的 creature/tag 范围，否则容易出现对错误单位触发的问题。

## 状态规则

实机确认前保持：

- `Target_QTD_FieryGoldenEyes` → `source-bound-reveal-draft`
- `QTD_STATUS_DEMON_REVEALED` → `invisibility-lock-ac-draft`
- `QTD_Passive_FieryGoldenEyes_TargetAdvantage` → `source-bound-target-advantage-draft`

不要标记 `toolkit-verified`。
