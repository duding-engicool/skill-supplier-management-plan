# 供应商管理方案生成技能（supplier-management-plan）

> 主色：#C8102E ｜ 范式：混合式（Markdown + HTML 双版）
> 面向供应商质量经理的供应商整体管理方案生成工具。

## 一句话说明
以九段式标准化框架覆盖分类分级、准入、绩效、审核、变更、协议、帮扶与应急，一键产出可归档的 MD 与可汇报的 HTML 双版方案。

## 适用角色
- 供应商质量经理（SQM）
- 采购质量负责人

## 使用场景
- 年度供应商质量管理规划
- 新业务线供应商体系搭建
- 现有体系复盘升级
- 管理体系受控文件起草

## 九段式框架
1. 管理目标与策略
2. 供应商分类与分级（来源：供应商质量画像）
3. 准入与选择（来源：供应商准入评估）
4. 绩效评价（来源：supplier-performance-evaluation）
5. 审核与监控（来源：supplier-audit）
6. 变更管理（来源：供应商变更管理）
7. 质量协议（联动：supplier-quality-agreement）
8. 发展帮扶（联动：supplier-development）
9. 风险与应急

## 文件清单
- `SKILL.md`：技能主文件
- `README.md`：本说明
- `scripts/build_report.py`：方案 JSON → MD + HTML 双版生成器

## 使用方法
```bash
# 内置小样本直接跑通，产出示意双版
python scripts/build_report.py

# 用自有数据
python scripts/build_report.py --input plan.json --md-out 供应商管理方案.md --html-out 供应商管理方案.html
```

## 联动技能
- supplier-quality-agreement（第7段协议条款）
- supplier-development（第8段帮扶机制）
- supplier-assessment（审核/评价口径一致）
- customer-satisfaction-survey（满意度下滑触发应急评审）

## 注意事项
- 企业特有阈值（PPM 红线、准时率、份额上限）标「待企业补充」，需企业填入后方可发布；
- 不编造标准号与真实供应商数据；
- 方案须经管理评审批准。
