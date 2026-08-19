# V0.3 七十二变子职业 / Seventy-Two Changes

## 定位

`QTD_SeventyTwoChanges` 是齐天大圣的变化专精路线。基础职业已经拥有小虫、苍鹰、猛虎和身外身法，因此子职业不复制这些能力，而是继续向同一个 `QTD_TransformContainer` 注入专属形态。

## Progression

| 等级 | 被动 | 新形态 | 定位 |
|---|---|---|---|
| L3 | `QTD_Passive_SeventyTwoChanges_L3` | 蜘蛛 | 蛛网、地形、探索 |
| L6 | `QTD_Passive_SeventyTwoChanges_L6` | 黑豹 | 潜行、伏击 |
| L10 | `QTD_Passive_SeventyTwoChanges_L10` | 枭熊、双脊龙 | 冲阵控制、高阶战斗 |

## Vanilla 对齐

- Spider: `Shout_WildShape_Combat_Spider` → `WILDSHAPE_SPIDER_GIANT_PLAYER`
- Panther: `Shout_WildShape_Combat_Panther` → `WILDSHAPE_PANTHER_PLAYER`
- Owlbear: `Shout_WildShape_Combat_Owlbear` → `WILDSHAPE_OWLBEAR_PLAYER_10`
- Dilophosaurus: `Shout_WildShape_Combat_Dilophosaurus` → `WILDSHAPE_DILOPHOSAURUS_PLAYER`
- 统一 Beast Shape Rules: `9c580a1d-dab9-4b17-b0da-b16c7d7360e0`

枭熊原版 SpellProperties 除了 Polymorph 之外还会附加 `OWLBEAR_WILDSHAPE_RAGE`，QTD 子条目保留这一 helper status。

## 仙力消耗

- 蜘蛛：1
- 黑豹：2
- 枭熊：2
- 双脊龙：3

所有形态仍然使用 Bonus Action 进入，不新增额外 Action/Bonus Action 上限，也不对整个职业提供全局仙力折扣。

## 兼容原则

- 所有新条目使用 `QTD_` TechName。
- 不覆盖 vanilla Wild Shape SpellData / StatusData。
- 继续复用现有 `QTD_TransformContainer` `1f3a673b-dc8b-4eca-9097-c6605a3de947`。
- 继承原版 Polymorph / 0 HP 恢复 / Hotbar / 装备处理链。
- 法天象地激活时禁止开始这些变化。
- 不要求 BG3 Script Extender。

## Toolkit 验证门

1. L3 子职业选择后 Spider child 正确出现在现有变化菜单。
2. L6 Panther 追加到同一菜单，不产生第二个容器。
3. L10 Owlbear + Dilophosaurus 同时追加。
4. 四个形态的 0 HP 恢复、手动退出、装备/Hotbar 恢复正常。
5. Owlbear Rage/Smash 等能力可用，退出后 helper status 清理。
6. Panther Prowl / invisibility 链正常。
7. Spider Web 与 web immunity 正常。
8. Dilophosaurus 攻击/投射能力正常。
9. 与三头六臂、法天象地、身外身法做组合回归。
