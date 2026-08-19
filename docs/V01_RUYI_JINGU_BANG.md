# V0.1 如意金箍棒 / Ruyi Jingu Bang

## 目标

`WPN_QTD_RuyiJinguBang` 是齐天大圣的 V0.1 核心主手武器。第一版优先保证 Stats、职业联动和可录入 RootTemplate，不要求自定义 3D 模型。

## Stats 定稿

- Stats parent: `WPN_Quarterstaff`
- Planning RootTemplate UUID: `521284c4-3d7b-4642-9c26-3677198f5a69`
- Rarity: Legendary
- Base damage: `1d8 Bludgeoning`
- Versatile damage: `1d10 Bludgeoning`
- Enchantment: `+2`
- Extra weapon damage: `1d4 Force`
- Strength: `+1`
- Jump distance: `x1.5`
- Weapon range: `300` = planned 3m melee range
- Weapon properties: `Versatile;Melee;Dippable;Reach;Magical`
- Unique: yes

实现位于 `src/stats/Weapons.txt`。

## 为什么继承 WPN_Quarterstaff

必须保持它是真正的 Quarterstaff，而不是只做成外观像长棍的自定义武器。这样：

1. `QTD_Passive_RuyiMastery` 的 `MonkWeaponAttackOverride()` 可以沿用成熟 Monk Weapon 路径。
2. Quarterstaff proficiency / Simple Weapon 语义由原版父 Stats 继承。
3. `Zone_QTD_SeaCalmingStrike` 可以读取真实 `MainMeleeWeapon` 与 `MainWeaponDamageType`。
4. V0.1 可以直接复用原版长棍动画、VisualTemplate 和 PhysicsTemplate。

## Reach 实现

原版 Reach 武器不是通过一个独立 `ReachBonus()` Boost 实现，而是武器 Stats 的 `WeaponRange` 配合 `Reach` property。

本项目第一版使用：

```txt
data "WeaponRange" "300"
data "Weapon Properties" "Versatile;Melee;Dippable;Reach;Magical"
```

目标是总近战距离 3m，即比普通 1.5m 近战多 1.5m。

## 跳跃修正

旧草稿中的：

```txt
JumpMaxDistance(1.5)
```

没有保留。第一版改为已有原版模式的：

```txt
JumpMaxDistanceMultiplier(1.5)
```

因此当前语义是跳跃距离 +50%，不是固定 +1.5m。

## 如意伸长

`Target_QTD_RuyiExtend` 不再是一个脱离武器的 `1d8 Force` 法术。第一版改为继承 `Target_MainHandAttack` 的 9m 主手武器攻击：

```txt
using "Target_MainHandAttack"
data "TargetRadius" "9"
data "SpellRoll" "Attack(AttackType.MeleeWeaponAttack)"
data "SpellSuccess" "DealDamage(MainMeleeWeapon, MainMeleeWeaponDamageType);ExecuteWeaponFunctors(MainHand)"
```

设计目标是让攻击继续走当前主手武器、如意兵法和武器附魔链，而不是复制另一套独立伤害公式。

## Toolkit RootTemplate 录入

原版 Quarterstaff RootTemplate 已确认：

- UUID: `96e2abaf-78ff-4dcb-a6a3-a5f0c348bd9f`
- Name: `WPN_HUM_Quarterstaff_A_0`
- Stats: `WPN_Quarterstaff`

在 Toolkit 中：

1. 克隆该 Quarterstaff RootTemplate。
2. 新 RootTemplate 目标 UUID 使用 `data/toolkit_item_recording.csv` 中的规划 UUID，若 Toolkit 自动生成不同 UUID，以 Toolkit 为准。
3. 将新 RootTemplate 的 `Stats` 改为 `WPN_QTD_RuyiJinguBang`。
4. V0.1 保留原版 Quarterstaff visual / physics / equipment type。
5. 设置物品名称和描述本地化。
6. 将 Toolkit 实际 UUID 回填 `data/toolkit_item_recording.csv` 和 `data/uuid_manifest.json`。
7. 再通过 `EQP_CC_QTD_GreatSage` 验证 Character Creation 初始装备。

## 手动验证清单

由项目所有者执行，不由 GitHub Actions 代替。

- [ ] Character Creation 获得金箍棒。
- [ ] 物品被识别为 Quarterstaff / Simple Weapon。
- [ ] 单手伤害为 1d8，双手为 1d10。
- [ ] 普通攻击只额外结算一次 `1d4 Force`。
- [ ] +2 enchantment 正确影响攻击/伤害。
- [ ] 装备时 STR +1，卸下后立即恢复。
- [ ] 跳跃距离按 x1.5 生效，卸下后恢复。
- [ ] 普通近战有效距离约为 3m。
- [ ] Opportunity Attack 的距离没有异常扩大或失效。
- [ ] `QTD_Passive_RuyiMastery` 在 STR/DEX 切换下仍正常。
- [ ] `Zone_QTD_SeaCalmingStrike` 使用金箍棒时读取正确武器伤害，Force rider 不重复。
- [ ] `Target_QTD_RuyiExtend` 可以在 9m 对敌人执行主手攻击。
- [ ] 如意伸长不会额外重复一份主手基础伤害或 `1d4 Force`。
- [ ] Save/Load、Respec、Multiclass 后没有永久残留 STR/Jump Boost。

验证完成前状态保持 `quarterstaff-root-draft`，不要标记 `toolkit-verified`。
