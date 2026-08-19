# V0.4 法天象地实现草案

## 目标

L11 的 `法天象地` 是齐天大圣基础职业的终极巨化战斗形态。第一版坚持 Stats 能解决的先用 Stats，不引入 Script Extender，也不修改玩家骨骼或真实装备槽。

## 激活

- 被动：`QTD_Passive_FaTianXiangDi`
- 主动：`Shout_QTD_FaTianXiangDi`
- 消耗：Action + 5 Sage Qi
- 持续：3 回合
- 每长休一次
- 与七十二变、隐形、身外身法的活动窗口、三头六臂互斥

长休冷却不用未验证的 SpellData 长休字符串，而是施法时附加隐藏状态 `QTD_STATUS_FATIAN_USED`，该状态使用已知的 `RemoveOnLongRest` 标记。

## 巨化状态

`QTD_STATUS_FATIAN_XIANG_DI` 第一版使用：

- `ObjectSize(+1)`
- `ScaleMultiplier(1.33)`
- `AbilityOverrideMinimum(Strength,25)`
- Strength Ability checks Advantage
- Strength Saving Throw Advantage
- Carry Capacity x2
- Frightened immunity
- 武器命中额外 `2d8 Force + 2d8 Thunder`

`ObjectSize(+1) + ScaleMultiplier(1.33)` 与原版 Enlarge 的公开数据模式对齐。它是当前可确认的安全巨化档，不把它虚标为已经验证的真正 Huge 碰撞体。真正的 Huge 视觉/碰撞在 Toolkit 实机阶段继续放大和测试。

## 专属动作

### 撼地

`Zone_QTD_FaTian_Quake`

- Action
- OncePerTurn
- 宽角冲击波
- STR Save
- 失败：4d8 Thunder + Prone + 3m knockback
- 成功：2d8 Thunder
- 第一版复用 `Zone_Thunderwave` 的几何/豁免链

### 横扫千军

`Zone_QTD_FaTian_Sweep`

- Action
- OncePerTurn
- 复用 `Zone_Cleave`
- 造成 `MainMeleeWeapon` 伤害并执行 MainHand Weapon Functors
- 120 度宽扫
- 击退 3m

### 擎天一柱

`Target_QTD_FaTian_Pillar`

- Action
- OncePerTurn
- 以 `Target_MainHandAttack` 为行为参考
- 计划目标距离 9m
- 造成主手武器伤害
- 击退 6m

9m 是法天象地“超长金箍棒”的专属技能距离，不等同于给所有普通近战动作增加 9m Reach。该数值需要 Toolkit 验证 inherited melee targeting flags。

## 互斥

为了避免复杂状态叠加：

- 七十二变子技能在法天象地期间禁用。
- 身外身法在施放时给本体添加 3 回合 `QTD_STATUS_HAIR_CLONES_ACTIVE`，法天象地检测该状态。
- 三头六臂与法天象地互相禁用。
- 法天象地检测 `SG_Invisible`，隐形期间不能启动。

这一方案不需要扫描召唤物，也不需要运行时脚本。

## 平衡边界

法天象地不会：

- 增加完整 ActionPoint
- 赋予 `ExtraAttack_2`
- 与三头六臂叠加
- 与七十二变叠加
- 在第一版宣称真正 Huge 碰撞体已经完成

大圣 L11 本身保留普通 Extra Attack。法天象地的爆发来自 3 回合的武器额外伤害和三个专属动作。

## Toolkit 验收

1. L10 看不到法天象地，L11 自动获得。
2. 激活准确消耗 Action + 5 Sage Qi。
3. 持续准确 3 回合。
4. 长休前不能再次使用，长休后恢复。
5. 模型/碰撞不会卡门、穿地或异常推开友军。
6. STR 低于 25 时提升到至少 25，高于 25 时不被降低。
7. 普通武器攻击获得 2d8 Force + 2d8 Thunder。
8. 撼地、横扫千军、擎天一柱只在状态存在时可用。
9. 退出形态后三个动作立即消失。
10. 与七十二变、隐形、身外身法、三头六臂的互斥全部符合预期。
11. `Target_QTD_FaTian_Pillar` 的 9m 实际目标距离可用。
12. 若要实现真正 Huge，再单独验证更大的 Scale/RootTemplate/碰撞方案。
