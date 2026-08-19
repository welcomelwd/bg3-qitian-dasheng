# V0.1 测试计划

## 0. 职业脊柱 Smoke Test

按 `docs/V01_CLASS_RESOURCE_SPINE.md` 先完成这组测试。任何一项失败，都先停止技能/装备扩展。

- [ ] `QTD_GreatSage` 出现在 Character Creation。
- [ ] 主职业和 Multiclass ClassDescriptions 使用不同 UUID。
- [ ] 两条 ClassDescriptions 都指向同一个主职业 Progression Table。
- [ ] `QTD_SageQi` 在 Action Resource 面板显示。
- [ ] L1 初始仙力 = 2。
- [ ] `Ctrl+Shift+L` 可逐级升到 L12，无空白奖励页、崩溃或 Stats/UUID 报错。
- [ ] L3 同时出现斗战胜佛、七十二变、灵明石猴。
- [ ] L4/L8/L12 出现 Feat。
- [ ] L5 获得 Extra Attack。
- [ ] L2/L3/L6 SpellList 正确进入技能栏。
- [ ] 仙力累计值依次为 L1 2 / L2 3 / L5 4 / L8 5 / L11 6。
- [ ] 当前 forward trunk 的 L12 封顶后仙力总上限 = 8。
- [ ] Short Rest 后仙力完全恢复。
- [ ] Respec 后资源上限和等级奖励重新计算，无旧状态残留。
- [ ] Multiclass 时仙力按 `QTD_GreatSage` 职业等级而不是角色总等级成长。
- [ ] Toolkit 实际 UUID 已回填 `data/toolkit_spine_recording.csv`。

## A. 创建角色

- [ ] 齐天大圣出现在 Character Creation。
- [ ] 名称、描述、图标正常。
- [ ] 主属性提示为 Strength，施法属性为 Wisdom。
- [ ] 初始装备正确。
- [ ] 多职业入口可选。

## B. 1–12 级升级

- [ ] 每一级都能正常完成升级，无空白/崩溃。
- [ ] 4/8/12 级出现 Feat。
- [ ] 5 级获得 Extra Attack。
- [ ] L2/L3/L6 技能按预期进入技能栏。
- [ ] 基础仙力最大值按 2/3/4/5/6 成长；当前 forward trunk L12 封顶后为 8。

## C. 仙力

- [ ] 消耗技能会正确扣除。
- [ ] 0 点时技能不可使用。
- [ ] 短休恢复完整。
- [ ] 长休后为满值。
- [ ] Respec 不残留旧资源上限。
- [ ] Multiclass 按大圣职业等级成长。

## D. 筋斗云

- [ ] Bonus Action + 1 仙力。
- [ ] 不能传送到非法位置。
- [ ] 传送后获得云势。
- [ ] 下一次近战攻击获得 Advantage，之后云势移除。
- [ ] L2/L5/L9/L12 距离按 12/15/18/21m 工作。

## E. 定海一棒

- [ ] Action + 2 仙力。
- [ ] 范围伤害正确。
- [ ] STR Save 正确。
- [ ] 失败时 Prone + Knockback。
- [ ] L5/L11 伤害成长正确。
- [ ] 最终版本包含预期的主手武器伤害组件。

## F. 火眼金睛

- [ ] Bonus Action + 1 仙力。
- [ ] 状态持续 3 回合。
- [ ] 目标 AC -2。
- [ ] 对隐形目标的行为符合设计。
- [ ] 大圣对标记目标攻击获得 Advantage，且不错误地给其他单位全局优势。

## G. 装备

- [ ] 金箍棒单手/双手伤害正确。
- [ ] 强化等级与额外 Force 伤害正确。
- [ ] 装备切换不会永久残留被动。
- [ ] 黄金甲与步云履不会造成错误叠加。
- [ ] Character Creation 初始装备链正确。

## H. 回归

- [ ] 单人新档。
- [ ] 4 人队伍。
- [ ] 多职业。
- [ ] Respec。
- [ ] Save/Load。
- [ ] Long Rest / Short Rest。
- [ ] 两个或更多齐天大圣角色不会共享错误的资源、子职业或变身容器状态。
