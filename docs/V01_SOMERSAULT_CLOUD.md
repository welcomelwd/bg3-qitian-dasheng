# V0.1 筋斗云 / Somersault Cloud

## 目标

`Target_QTD_SomersaultCloud` 是齐天大圣 L2 的基础机动技能。V0.1 只要求稳定完成三件事：

1. Bonus Action + 1 `QTD_SageQi` 的可选落点传送；
2. 落地后获得 1 回合 `QTD_STATUS_CLOUD_MOMENTUM`；
3. 距离随 Great Sage 等级按 12m → 15m → 18m → 21m 成长。

不依赖 Script Extender。

## Stats 结构

### 主技能

```txt
new entry "Target_QTD_SomersaultCloud"
type "SpellData"
using "Target_MistyStep"
data "TargetRadius" "12"
data "UseCosts" "BonusActionPoint:1;QTD_SageQi:1"
data "SpellProperties" "TeleportSource();ApplyStatus(SELF,QTD_STATUS_CLOUD_MOMENTUM,100,1)"
```

`Target_MistyStep` 继续作为选点传送的原版行为参考。

### 云势

```txt
new entry "QTD_STATUS_CLOUD_MOMENTUM"
type "StatusData"
data "StatusType" "BOOST"
data "Boosts" "IF(IsMeleeAttack()):Advantage(AttackRoll)"
data "Passives" "QTD_Passive_CloudMomentum_Consume"
```

隐藏 helper：

```txt
new entry "QTD_Passive_CloudMomentum_Consume"
type "PassiveData"
data "Properties" "IsHidden"
data "StatsFunctorContext" "OnAttack"
data "Conditions" "IsMeleeAttack()"
data "StatsFunctors" "RemoveStatus(SELF,QTD_STATUS_CLOUD_MOMENTUM)"
```

设计语义是：远程攻击不获得优势，也不消费云势；首次近战攻击获得优势并消费云势。

## 距离成长

不创建 4 个不同的筋斗云 Spell。使用同一个 Spell，并在等级 progression 中追加隐藏 `UnlockSpellVariant`：

| Great Sage 等级 | 新增倍率 | 累积目标距离 |
|---|---:|---:|
| L2 | base | 12m |
| L5 | ×1.25 | 15m |
| L9 | ×1.2 | 18m |
| L12 | ×1.1666667 | ≈21m |

对应隐藏被动：

- `QTD_Passive_SomersaultCloud_Range_L5`
- `QTD_Passive_SomersaultCloud_Range_L9`
- `QTD_Passive_SomersaultCloud_Range_L12`

使用公开 BG3 Stats 已存在的：

```txt
UnlockSpellVariant(SpellId('...'),ModifyTargetRadius(Multiplicative,...),)
```

这一做法的目标是保持热栏里始终只有一个筋斗云。

## Patch 8 Toolkit 验收

### 基础施放

- [ ] L1 不存在筋斗云；L2 正确解锁。
- [ ] 使用消耗 1 Bonus Action。
- [ ] 使用消耗 1 Sage Qi。
- [ ] 能选择合法地面落点，不能错误穿入不可站立区域。
- [ ] 传送动画 / VFX / 目标预览继承链正常。

### 距离

- [ ] L2 最大目标距离约 12m。
- [ ] L5 最大目标距离约 15m。
- [ ] L9 最大目标距离约 18m。
- [ ] L12 最大目标距离约 21m。
- [ ] 升级后热栏仍只有一个 `Target_QTD_SomersaultCloud`。
- [ ] Save/Load 后倍率不重复叠加。
- [ ] Respec 降级后旧倍率不会残留。
- [ ] Multiclass 时按 `QTD_GreatSage` 实际等级获得 L5/L9/L12 的距离被动，而不是按总角色等级。

### 云势

- [ ] 传送完成后本体获得 `QTD_STATUS_CLOUD_MOMENTUM`。
- [ ] 云势持续 1 回合。
- [ ] 下一次近战武器攻击显示 Advantage。
- [ ] 下一次近战徒手攻击显示 Advantage。
- [ ] 近战攻击命中后云势消失。
- [ ] 近战攻击未命中后云势也消失。
- [ ] 在云势期间先进行远程攻击，不获得 Advantage，且云势不被消费。
- [ ] 在云势期间先施放法术，不应错误消费云势。
- [ ] 超过持续时间未进行近战攻击时云势正常过期。

### 组合回归

- [ ] 如意兵法使用 DEX 时，云势仍只影响 Advantage，不改变攻击属性选择。
- [ ] L5 Extra Attack 下，云势只强化第一次近战攻击，不强化整个 Attack action 的全部攻击。
- [ ] 三头六臂状态下，云势仍只能消费一次。
- [ ] 斗战胜佛暴击链不会导致云势重复消费。
- [ ] 灵明石猴的强化云遁技能与基础筋斗云状态 StackId 不产生重复 Advantage。

## Toolkit Gate

当前状态：`momentum-range-scaling-draft`。

以下内容没有在仓库侧假装为已验证：

1. `TeleportSource();ApplyStatus(SELF,...)` 的实际执行顺序；
2. `OnAttack` cleanup 是否在攻击骰读取 Advantage 之后触发；
3. 三个 `ModifyTargetRadius(Multiplicative,...)` 是否按预期累计，并在 L12 稳定显示为约 21m；
4. Respec / Multiclass 对隐藏距离被动的真实增删行为。

只有完成上述 Toolkit/游戏检查后才可升级为 `toolkit-verified`。
