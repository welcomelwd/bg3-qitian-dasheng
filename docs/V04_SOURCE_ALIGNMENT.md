# V0.4 法天象地数据来源对齐

本文件只记录公开 BG3 数据中已经出现过的语法/模式，不代表本机 Patch 8 Toolkit 已完成实机验证。

- 原版 `ENLARGE`：`ObjectSize(+1)`、`ScaleMultiplier(1.33)`、Strength Advantage、额外 CharacterWeaponDamage。
- 公开 Weapon Stats：`AbilityOverrideMinimum(Strength,18)`，V0.4 据此采用同语法的 Strength 25 下限草案。
- 原版 Rush 武器动作：`DealDamage(MainMeleeWeapon, MainMeleeWeaponDamageType)` + `ExecuteWeaponFunctors(MainHand)`。
- `Zone_Cleave` 派生动作：支持多目标主手武器伤害与 Weapon Functors。
- `SG_Invisible`：原版 Invisible StatusGroup。
- `RemoveOnLongRest`：已存在的 StatusPropertyFlags，用于 V0.4 的一次/长休使用标记。
- `OncePerTurn`：已存在的 SpellData Cooldown 值，用于三个形态专属动作。

因此 V0.4 第一版避免使用尚未验证的：

- `ObjectSize(+2)`
- 猜测式通用 melee reach Boost
- 猜测式 SpellData `OncePerLongRest` Cooldown 字符串
- 额外完整 ActionPoint
- Script Extender 运行时体型/装备复制
