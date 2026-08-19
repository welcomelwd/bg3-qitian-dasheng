# V0.1 灵猴身法运行时收口

目标：把 `QTD_Passive_MonkeyAgility` 从概念 Stats 草案推进到 Patch 8 Toolkit 可直接验证的原版模式实现。

## 当前实现

### 可见被动

`QTD_Passive_MonkeyAgility`

- AC 公式：`ACOverrideFormula(10,true,Dexterity,Wisdom)`
- `BoostContext = OnEquip;OnCreate`
- 仅在未穿护甲且未持盾时生效：
  - `not WearingArmor(context.Source)`
  - `not HasShieldEquipped(context.Source)`

目标结果：未着甲 AC = 10 + DEX Modifier + WIS Modifier。

### 隐藏移动 helper

`QTD_Passive_MonkeyAgility_Mobility`

- `ActionResource(Movement,3,0)`：+3m 移动
- `JumpMaxDistanceMultiplier(1.5)`：跳跃距离 ×1.5
- `FallDamageMultiplier(0.5)`：坠落伤害 ×0.5

helper 独立于未着甲 AC 条件，因此穿甲/持盾只应关闭 AC 公式，不应删除基础移动、跳跃和坠落减伤。

## 为什么拆成两个 Passive

如果把 `BoostConditions` 放在同一个 Passive 上，条件会同时影响 AC、移动、跳跃和坠落减伤。拆成隐藏 helper 后，装备切换只需要验证 AC 开关，其他灵猴机动效果保持稳定。

## Patch 8 Toolkit 验收

1. L1 获得一个可见“灵猴身法”，隐藏 helper 不应单独污染 UI。
2. 裸装、无盾时，AC 等于 `10 + DEX mod + WIS mod`。
3. 穿任意 Armor 后，额外 WIS AC 立刻消失。
4. 卸下 Armor 后，AC 立即恢复。
5. 装备 Shield 后，未着甲 AC 公式关闭；卸盾后恢复。
6. 移动距离相对基础值 +3m。
7. 跳跃最大距离约为基础值 ×1.5。
8. 从同一高度分别测试有/无本被动角色，悟空坠落伤害应约为对照组 50%。
9. Save/Load、Respec、Multiclass 后重复装备切换，不能残留 AC。
10. 与黄金甲测试时确认“穿甲关闭 AC”符合预期，不发生双重 AC 叠加。

通过以上测试前，状态保持 `vanilla-pattern-aligned-draft`，不得标记 `toolkit-verified`。
