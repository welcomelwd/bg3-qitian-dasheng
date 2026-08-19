# 斗战胜佛 Toolkit 验证清单

## 子职业入口
- [ ] L3 升级界面出现 `QTD_VictoriousBuddha`
- [ ] 选择后 Character Sheet 显示斗战胜佛
- [ ] `ParentUUID` 正确指向齐天大圣主职业
- [ ] subclass ProgressionTableUUID 与 L3/L6/L10 三行一致

## L3 斗战棍法
- [ ] 普通近战暴击额外增加 1 个武器伤害骰
- [ ] 暴击额外骰不会重复触发两次
- [ ] 远程攻击不获得额外骰
- [ ] 后续验证 Quarterstaff / Ruyi 条件后再决定是否收窄武器范围

## L6 战意无双
- [ ] 自然骰 19 可暴击
- [ ] 自然骰 18 不暴击
- [ ] 与装备降低暴击阈值的效果测试叠加方式
- [ ] 与三头六臂多次攻击不会异常重复添加阈值

## L10 破天一棒
- [ ] 消耗 1 Action + 2 Sage Qi
- [ ] 每回合最多使用一次
- [ ] 命中结算主手武器伤害
- [ ] `ExecuteWeaponFunctors(MainHand)` 不重复基础武器伤害
- [ ] 额外造成 2d8 Force
- [ ] 施加 `QTD_STATUS_HEAVEN_BREAK_ARMOR` 2 回合
- [ ] `AC(-2)` 在 Patch 8 Toolkit 中确实降低目标 AC 2 点
- [ ] 状态结束后 AC 正确恢复

## 组合回归
- [ ] 三头六臂 + 斗战胜佛
- [ ] 法天象地 + 斗战胜佛
- [ ] Haste + 破天一棒
- [ ] Action Surge + 破天一棒
- [ ] 金箍棒附魔 + 破天一棒
- [ ] 暴击装备 + 战意无双

只有完成以上实机验证后，相关状态才能从 draft 升级为 `toolkit-verified`。
