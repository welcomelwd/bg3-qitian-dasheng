# V0.1 定海一棒 / Sea-Calming Strike

## 目标

`Zone_QTD_SeaCalmingStrike` 是 L3 基础职业主动技：

- Action ×1
- QTD_SageQi ×2
- 继承 `Zone_Cleave` 的近战扇区基础结构
- 3m / 120°
- 对敌方角色造成主手武器伤害
- 额外 Thunder 伤害随 Great Sage 等级成长
- STR 豁免失败：Prone 1 回合 + 3m 击退
- STR 豁免成功：只将额外 Thunder 伤害减半，主手武器伤害仍完整结算

## 等级成长

| Great Sage 等级 | Thunder |
|---|---:|
| 3-4 | 2d8 |
| 5-10 | 3d8 |
| 11-12 | 4d8 |

成长只读取 `QTD_GreatSage` class level，不按总角色等级增长。

## 当前实现

武器部分：

```txt
DealDamage(MainMeleeWeapon,MainWeaponDamageType)
GROUND:ExecuteWeaponFunctors(MainHand)
```

雷鸣成长通过 `ClassLevelHigherOrEqualThan(...)` 三档条件选择。

控制只存在于 failed save 分支：

```txt
ApplyStatus(PRONE,100,1)
Force(3,OriginToEntity,Aggressive,true)
```

## 项目所有者实机验证清单

1. L3、L4 的额外雷鸣必须为 2d8。
2. L5-L10 必须为 3d8。
3. L11-L12 必须为 4d8。
4. 成功 STR 豁免：武器伤害完整，Thunder 减半，不倒地、不击退。
5. 失败 STR 豁免：武器伤害完整，Thunder 全额，Prone + 3m Force。
6. 3m / 120° 扇区预览和实际命中区域一致。
7. 多目标命中时，每个目标只结算一次主手武器伤害。
8. 多目标命中时，武器附魔/被动 functor 不应出现意外多次触发或指数级触发。
9. 如意金箍棒、普通 Quarterstaff、其他近战武器各测一次。
10. 无主手武器时检查技能是否应该禁用；若当前表现异常，再增加更严格 RequirementConditions。
11. Haste / Extra Attack 不应改变本技能自身一次 Action 的单次释放语义。
12. Respec / multiclass 后确认成长读取 Great Sage class level，而不是 CharacterLevel。

## 状态规则

在项目所有者完成 Patch 8 Toolkit / 游戏验证前，保持：

`weapon-zone-scaling-draft`

不要标记 `toolkit-verified`。
