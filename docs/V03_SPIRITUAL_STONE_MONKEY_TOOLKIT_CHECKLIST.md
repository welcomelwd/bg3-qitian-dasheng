# V0.3 灵明石猴 Toolkit Checklist

## 子职业入口
- [ ] L3 同时出现斗战胜佛、七十二变、灵明石猴
- [ ] `QTD_SpiritualStoneMonkey` ParentUUID 指向主职业
- [ ] Progression Table 为 `dc1d9370-6736-4197-b805-25b0e00fd355`
- [ ] L3/L6/L10 均为 ProgressionType=1
- [ ] Character Sheet 正确显示灵明石猴

## L3 灵台悟法
- [ ] Spell Save DC 实际 +1
- [ ] Melee Spell Attack 实际 +1
- [ ] Ranged Spell Attack 实际 +1
- [ ] 不影响普通武器 Attack Roll
- [ ] 三昧真火消耗 Action + 2 Sage Qi
- [ ] 三昧真火不消耗 SpellSlot
- [ ] Burning Hands 锥形范围、DEX save、火焰 VFX 正常

## L6 风雷云遁
- [ ] 风雷云遁消耗 Bonus Action + 2 Sage Qi
- [ ] 18m 目标范围生效
- [ ] 传送后 `QTD_STATUS_CLOUD_SPELL_MOMENTUM` 施加到施法者
- [ ] Momentum 持续恰好 1 回合
- [ ] Momentum 的 Spell Save DC / Spell Attack / Movement 增益正确
- [ ] 重复施放不叠层
- [ ] 掌心雷消耗 Action + 2 Sage Qi
- [ ] 掌心雷不消耗 SpellSlot

## L10 五行圆融
- [ ] 菜单只显示 5 个 QTD 子法术
- [ ] 不显示原版 Monk/Ki 子条目
- [ ] 五个子法术均消耗 Action + 3 Sage Qi
- [ ] 不消耗 Ki
- [ ] 不消耗 SpellSlot
- [ ] Fire / Cold / Lightning / Thunder / Acid 伤害类型正确
- [ ] level-4 Chromatic Orb 伤害与 surface 行为正常
- [ ] QTD RootSpellID 清理后没有错误的 upcast/UI grouping

## 组合回归
- [ ] 灵台悟法 + 风雷云遁的 +1/+1 是否按预期合计
- [ ] Haste 不导致免费仙术或额外资源恢复
- [ ] 法天象地次数不被刷新
- [ ] Respec 后子职业技能全部清理
- [ ] Multiclass 不错误授予 SpellSlot
- [ ] Multiplayer 两名灵明石猴互不污染状态/容器
