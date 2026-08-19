# V0.4 法天象地实机测试矩阵

| 场景 | 预期 |
|---|---|
| L10 | 不存在法天象地主动技能 |
| L11 | 被动解锁 `Shout_QTD_FaTianXiangDi` |
| 激活 | 消耗 Action + 5 Sage Qi |
| 持续时间 | 3 rounds |
| 再次使用 | 长休前被 `QTD_STATUS_FATIAN_USED` 阻止 |
| 长休 | `RemoveOnLongRest` 清除使用标记 |
| STR 20 | 形态内至少 25 |
| STR 27 | 不应被降低到 25 |
| 普通武器攻击 | +2d8 Force +2d8 Thunder |
| 撼地失败 STR Save | 4d8 Thunder + Prone + 3m knockback |
| 撼地成功 STR Save | 2d8 Thunder |
| 横扫千军 | 主手武器伤害 + Weapon Functors + 3m knockback |
| 擎天一柱 | 计划 9m 目标距离 + 主手伤害 + 6m knockback |
| 七十二变中 | 法天象地不可启动 |
| 法天象地中 | 三个 QTD 变身子技能不可启动 |
| 隐形中 | 法天象地不可启动 |
| 毫毛分身活动窗口 | 法天象地不可启动 |
| 法天象地中 | 身外身法不可启动 |
| 三头六臂中 | 法天象地不可启动 |
| 法天象地中 | 三头六臂不可启动 |
| Haste / Action Surge | 不产生额外非法 Action 或无限攻击链 |
| 狭窄门洞/楼梯 | 巨化模型和碰撞不锁死角色 |

## 尚未宣称完成

- 真正 Huge 碰撞体
- 9m 近战继承 flags 的最终行为
- 法天象地只对如意金箍棒追加元素伤害的精确条件
- 最终巨化 VFX / Camera / Animation
