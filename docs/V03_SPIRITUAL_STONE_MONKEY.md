# V0.3 灵明石猴 / Spiritual Stone Monkey

## 定位

第三子职业走 Wisdom 仙术路线，不依赖额外攻击，也不扩充 Wild Shape。核心循环是：

1. 以 Wisdom 提高 QTD 仙术命中与豁免 DC。
2. 使用 Sage Qi 施展三昧真火、掌心雷等法术。
3. 通过风雷云遁重定位并获得 1 回合施法强化。
4. L10 进入五行仙法容器，在五种元素显化间选择。

## L3 — 灵台悟法

`QTD_Passive_SpiritualStoneMonkey_L3`

- `SpellSaveDC(1)`
- `RollBonus(MeleeSpellAttack,1)`
- `RollBonus(RangedSpellAttack,1)`
- 解锁 `Zone_QTD_SamadhiFire`
- 三昧真火：Action + 2 Sage Qi
- Base: `Zone_BurningHands`

该 Boost 组合来自 BG3 已存在的 Arcane Enchantment 被动模式。

## L6 — 风雷云遁

`QTD_Passive_SpiritualStoneMonkey_L6` 解锁强化筋斗云与掌心雷。

- `Target_QTD_CloudThunderStep`：Bonus Action + 2 Sage Qi，18m，施放后计划附加 `QTD_STATUS_CLOUD_SPELL_MOMENTUM` 1 回合。
- `Projectile_QTD_PalmThunder`：Action + 2 Sage Qi，继承 `Projectile_ChromaticOrb_Lightning`。

Momentum 提供 Spell Save DC +1、Melee/Ranged Spell Attack +1、Movement +3m，并通过 StackId 防止叠层。

`ApplyStatus(SELF,...)` 在传送后的具体时序仍需 Patch 8 Toolkit 实测。

## L10 — 五行圆融

`QTD_Passive_SpiritualStoneMonkey_L10` 解锁 `Projectile_QTD_FiveElements`。

容器继承 `Projectile_ChromaticOrb_Monk` 的资源型元素选择结构，但不使用 Ki 或 SpellSlot。每个子法术固定 Action + 3 Sage Qi。

| QTD 法术 | Base |
|---|---|
| 火行·真焰 | `Projectile_ChromaticOrb_Fire_4` |
| 水行·玄冰 | `Projectile_ChromaticOrb_Cold_4` |
| 雷行·天雷 | `Projectile_ChromaticOrb_Lightning_4` |
| 风行·震空 | `Projectile_ChromaticOrb_Thunder_4` |
| 土行·蚀地 | `Projectile_ChromaticOrb_Acid_4` |

使用 level-4 Chromatic Orb 作为 L10 强度参考，目标约为 5d8 等级的单体元素爆发及对应 surface 行为；最终以 Toolkit 实机为准。

## 平衡护栏

- 不授予 Spell Slots。
- 不增加 Action / Bonus Action。
- 不授予 `ExtraAttack_2`。
- 不全局降低 Sage Qi 消耗。
- 不刷新法天象地长休次数。
- 风雷云遁强化不叠层。
- 与基础职业共享同一个 `QTD_SageQi` 池。

## 运行状态

`subclass-wired-draft`

待本机 Patch 8 Toolkit 验证后才能升级为 `toolkit-verified`。
