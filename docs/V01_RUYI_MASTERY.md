# V0.1 如意兵法运行时收口

目标：让 `QTD_Passive_RuyiMastery` 在不强制 Finesse、不硬编码永久 DEX 的情况下，复用成熟 Monk Weapon 攻击属性切换模式。

## 当前实现

`QTD_Passive_RuyiMastery`

- 条件：`IsDexterityGreaterThanStrength()`
- Boost：`MonkWeaponAttackOverride()`
- BoostContext：`OnStatusApply;OnStatusRemove;OnEquip;OnShortRest;OnCreate;OnLongRest;OnInventoryChanged`

逻辑：

1. `DEX > STR`：对引擎判定为 Monk Weapon 的武器启用敏捷攻击属性覆盖。
2. `DEX <= STR`：条件不成立，不写任何覆盖，武器保持自然的 Strength 路径。
3. 不使用永久 `WeaponAttackRollAbilityOverride(Dexterity)`。
4. 不为了属性选择给所有武器增加 `Finesse`。

## 为什么采用 Monk Weapon 路线

公开成熟的 Monk Martial Arts 数据使用同一组：

- `IsDexterityGreaterThanStrength()`
- `MonkWeaponAttackOverride()`

这比自己计算 `max(STR,DEX)` 更接近游戏已有的武僧武器系统，也能在属性变化、换武器、休息和状态变化时重新评估。

## V0.1 目标范围

设计重点仍然是：

- 普通 Quarterstaff
- `WPN_QTD_RuyiJinguBang`

但 `MonkWeaponAttackOverride()` 的实际适用范围由 BG3 的 Monk Weapon 规则决定，所以首版必须做一个非长棍的 monk-eligible 简单武器对照测试。如果范围比设计预期更宽，再在 Toolkit 中寻找可靠的 Quarterstaff-only 谓词；在找到之前不猜内部条件名。

## Patch 8 Toolkit 验收

### A. 属性切换

1. STR 16 / DEX 12，普通 Quarterstaff：攻击与伤害保持 STR。
2. STR 12 / DEX 16，普通 Quarterstaff：攻击与伤害切到 DEX。
3. STR 16 / DEX 16：保持自然 STR 路径，不强制 DEX。
4. 战斗外换装备、施加/移除属性状态后重新检查面板和实际命中。

### B. 金箍棒

5. 给 `WPN_QTD_RuyiJinguBang` 设置真实 Quarterstaff Parent 后重复 A 组测试。
6. 金箍棒的 +1 STR 不得导致 DEX 路线错误锁死；最终比较必须按角色当时实际 STR/DEX。
7. 如意伸长和其他 Weapon Action 应使用同一武器攻击属性逻辑，不出现普通攻击用 DEX、武器动作却偷偷用 STR 的分裂。

### C. 范围控制

8. 使用至少一个非 Quarterstaff、但可能符合 Monk Weapon 规则的简单近战武器做对照。
9. 如果该武器也切到 DEX，记录为 built-in scope，不先判定为 bug；决定 V0.1 是否接受 Monk Weapon 全范围，或后续加可靠 Quarterstaff-only gate。
10. Heavy / Two-Handed 等明确不应成为 Monk Weapon 的武器不能被异常改成 DEX。

### D. 生命周期

11. Save/Load 后结果一致。
12. Respec 后结果按新 STR/DEX 重新计算。
13. Multiclass 后只要仍持有 `QTD_Passive_RuyiMastery`，逻辑应稳定；移除大圣等级/被动后不得残留覆盖。

通过上述测试前，状态保持 `monk-weapon-pattern-aligned-draft`，不得标记 `toolkit-verified`。
