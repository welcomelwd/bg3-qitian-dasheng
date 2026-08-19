# V0.3 斗战胜佛 / Victorious Fighting Buddha

## 定位

斗战胜佛是齐天大圣的纯近战子职业。它不增加新的变化资源，也不复制法天象地的巨化能力，而是把已有的棍战体系推向暴击与单体破防。

## 官方 Toolkit 结构

- 独立 subclass Progression TableUUID：`7761cb09-7c56-4ff5-b4eb-8860683eed61`
- subclass Progression rows 使用 `ProgressionType=1`
- 首行等级为 3
- `QTD_GreatSage_3.SubClasses` 加入 `QTD_VictoriousBuddha`
- ClassDescriptions 新增 `QTD_VictoriousBuddha`，`ParentUUID` 指向主职业 ClassDescriptions UUID

## 等级能力

### L3 斗战棍法

`QTD_Passive_VictoriousBuddha_StaffFury`

首版使用公开 BG3 数据中 `SavageAttacks` 同源模式：

`CriticalHitExtraDice(1,MeleeWeaponAttack)`

效果：近战武器暴击时额外增加一个武器伤害骰。

当前技术边界：首版覆盖所有 melee weapon attack。只有在 Toolkit 中验证可靠的 quarterstaff / Ruyi weapon condition 后，才收窄为棍棒专属，避免猜内部 weapon-type 条件。

### L6 战意无双

`QTD_Passive_VictoriousBuddha_ImprovedCritical`

直接继承原版 `ImprovedCritical`。公开 Patch 8 数据中该被动的核心 Boost 为：

`ReduceCriticalAttackThreshold(1)`

预期将常规暴击区间从 20 扩展为 19-20。

### L10 破天一棒

由 `QTD_Passive_VictoriousBuddha_HeavenBreaker` 解锁 `Target_QTD_HeavenBreakingStrike`。

- Action ×1
- Sage Qi ×2
- OncePerTurn
- 造成主手武器伤害
- 执行主手 Weapon Functors
- 额外 2d8 Force
- 命中后附加 `QTD_STATUS_HEAVEN_BREAK_ARMOR` 2 回合
- 首版破甲：AC -2

`AC(-2)` 必须在本机 Patch 8 Toolkit 中验证。公开数据已经确认 `AC(n)` Boost 家族存在，但负数仍保留为 runtime validation gate。

## 平衡限制

斗战胜佛不会：

- 增加额外 Action 或 Bonus Action
- 提供 `ExtraAttack_2`
- 增加仙力上限
- 在 L10 再次降低暴击阈值
- 自动刷新三头六臂或法天象地

因此它的高等级爆发来自已有 Extra Attack + 更高暴击率 + 破天一棒，而不是继续膨胀动作经济。

## Toolkit 验收

1. L3 升级时能选择斗战胜佛。
2. Character Sheet 显示正确子职业名。
3. L3 暴击额外骰只触发一次。
4. L6 常规武器攻击 19 点自然骰能暴击，18 点不能。
5. L10 破天一棒正确消耗 2 Sage Qi 与 1 Action。
6. Weapon Functors 与额外 2d8 Force 不重复计算基础武器伤害。
7. `QTD_STATUS_HEAVEN_BREAK_ARMOR` 正确降低 2 AC，2 回合后移除。
8. Haste / Action Surge 下破天一棒仍受 OncePerTurn 限制。
9. 与三头六臂、法天象地、金箍棒附魔组合时无无限攻击或重复暴击骰。
