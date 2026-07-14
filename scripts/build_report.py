#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
供应商管理方案生成器
读入结构化方案 JSON，生成 Markdown 文档 + 纯文字版 TXT。

用法：
  python build_report.py --input plan.json --out-dir ./out
  python build_report.py                                  # 不传参数，使用内置小样本，直接产出 txt+md

输入 JSON 结构：
{
  "plan_title": "2026年度供应商质量管理方案",
  "owner": "供应商质量部",
  "period": "2026年度",
  "objectives": ["目标1", "目标2"],
  "supplier_overview": "供应商总体概况描述",
  "sections": [
    {"no":"01","title":"管理目标与策略","body":"段落说明","bullets":["要点1","要点2"]},
    ...
  ],
  "timeline": [{"phase":"阶段","time":"时间","task":"任务"}],
  "pending": ["待企业补充项1", "待企业补充项2"]
}
"""

import argparse
import json
import os
import sys
from datetime import datetime


def load_plan(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def bullets_md(items):
    if not items:
        return "（待企业补充）"
    return "\n".join(f"- {it}" for it in items)


def build_md(p):
    L = []
    L.append(f"# {p.get('plan_title','供应商管理方案')}\n")
    L.append("## 一、方案概览\n")
    L.append(f"- 责任部门：{p.get('owner','')}")
    L.append(f"- 适用周期：{p.get('period','')}")
    L.append(f"- 生成日期：{datetime.now().strftime('%Y-%m-%d')}\n")
    L.append("## 二、管理目标\n")
    for o in p.get("objectives", []) or []:
        L.append(f"- {o}")
    if not p.get("objectives"):
        L.append("- （待企业补充）")
    L.append("")
    L.append("## 三、供应商总体概况\n")
    L.append(p.get("supplier_overview", "（待企业补充）"))
    L.append("")
    L.append("## 四、管理方案框架（九段式）\n")
    for s in p.get("sections", []) or []:
        L.append(f"### {s.get('no','')} {s.get('title','')}\n")
        body = s.get("body")
        if body:
            L.append(f"{body}\n")
        L.append(bullets_md(s.get("bullets", [])))
        L.append("")
    L.append("## 五、实施时间线\n")
    L.append("| 阶段 | 时间 | 主要任务 |")
    L.append("|------|------|----------|")
    for t in p.get("timeline", []) or []:
        L.append(f"| {t.get('phase','')} | {t.get('time','')} | {t.get('task','')} |")
    L.append("")
    pend = p.get("pending", [])
    if pend:
        L.append("## 六、待企业补充项\n")
        for x in pend:
            L.append(f"- 〔待企业补充〕{x}")
        L.append("")
    L.append(f"> 本报告由供应商管理方案技能生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(L)


def build_txt(p):
    W = 56
    L = []
    title = p.get("plan_title", "供应商管理方案")
    L.append("=" * W)
    L.append(title)
    L.append("=" * W)
    L.append("")
    L.append("一、方案概览")
    L.append("-" * W)
    L.append(f"责任部门：{p.get('owner','')}")
    L.append(f"适用周期：{p.get('period','')}")
    L.append(f"生成日期：{datetime.now().strftime('%Y-%m-%d')}")
    L.append("")
    L.append("二、管理目标")
    L.append("-" * W)
    objs = p.get("objectives", []) or []
    if objs:
        for o in objs:
            L.append(f"- {o}")
    else:
        L.append("- （待企业补充）")
    L.append("")
    L.append("三、供应商总体概况")
    L.append("-" * W)
    L.append(p.get("supplier_overview", "（待企业补充）"))
    L.append("")
    L.append("四、管理方案框架（九段式）")
    L.append("-" * W)
    for s in p.get("sections", []) or []:
        L.append(f"{s.get('no','')} {s.get('title','')}")
        body = s.get("body")
        if body:
            L.append(body)
        items = s.get("bullets", []) or []
        if items:
            for it in items:
                L.append(f"  - {it}")
        else:
            L.append("  - （待企业补充）")
        L.append("")
    L.append("五、实施时间线")
    L.append("-" * W)
    for t in p.get("timeline", []) or []:
        L.append(f"〔{t.get('phase','')}｜{t.get('time','')}〕{t.get('task','')}")
    L.append("")
    pend = p.get("pending", [])
    if pend:
        L.append("六、待企业补充项")
        L.append("-" * W)
        for x in pend:
            L.append(f"- 〔待企业补充〕{x}")
        L.append("")
    L.append(f"本报告由供应商管理方案技能生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(L)


# 内置小样本：可直接跑通产出 txt+md 示意文档
SAMPLE_PLAN = {
    "plan_title": "2026年度供应商质量管理方案（示意）",
    "owner": "供应商质量部",
    "period": "2026年度",
    "objectives": [
        "建立统一的供应商分类分级与绩效评价口径",
        "将低绩效（C/D级）供应商整改关闭率提升至90%以上",
        "重大4M1E变更通知及时率100%"
    ],
    "supplier_overview": "现有供应商约120家，其中A级35家、B级55家、C级25家、D级5家；主要风险集中在C/D级供应商的过程稳定性与变更管理。",
    "sections": [
        {"no": "01", "title": "管理目标与策略", "body": "以风险为导向，差异化管控。",
         "bullets": ["A级：常规监控、优先订单", "C/D级：加严检验+限期整改", "策略对齐企业质量方针（待企业补充）"]},
        {"no": "02", "title": "供应商分类与分级", "body": "参考供应商质量画像六维度（质量表现/问题模式/改善意愿/合作态度/交付表现/综合风险）。",
         "bullets": ["A级(≥8.0)：维持合作", "B级(6.0-7.9)：常规管理", "C级(4.0-5.9)：加严+改善期限", "D级(<4.0)：减份额/备选/暂停"]},
        {"no": "03", "title": "准入与选择", "body": "参考供应商准入评估：资质初审→现场审核(QSA+QPA)→样品验证。",
         "bullets": ["强制IATF16949（汽车行业，待企业补充）", "现场审核绿灯(≥80%)方可批准"]},
        {"no": "04", "title": "绩效评价", "body": "五维度加权：质量30%/交付25%/价格20%/服务15%/技术10%。",
         "bullets": ["A级≥90 / B级80-89 / C级70-79 / D级<70", "红黄牌触发机制见绩效评价体系"]},
        {"no": "05", "title": "审核与监控", "body": "参考supplier-audit：QSA/QPA/产品审核，ABCD分级。",
         "bullets": ["年度QSA + 关键过程QPA", "C级供应商季度审核"]},
        {"no": "06", "title": "变更管理", "body": "参考供应商变更管理：4M1E识别，I/II/III级分级。",
         "bullets": ["I级变更：客户书面批准+PPAP", "II级：7日内无异议可实施", "III级：备案即可"]},
        {"no": "07", "title": "质量协议", "body": "联动supplier-quality-agreement。",
         "bullets": ["质量标准/不合格处理/索赔/审核权/变更通知五大核心条款"]},
        {"no": "08", "title": "发展帮扶", "body": "联动supplier-development，针对低绩效供方。",
         "bullets": ["制定提升计划→里程碑跟踪→效果验证"]},
        {"no": "09", "title": "风险与应急", "body": "备选供应商库与淘汰机制。",
         "bullets": ["D级连续2次启动淘汰", "重大质量事故暂停供货"]}
    ],
    "timeline": [
        {"phase": "Q1", "time": "1-3月", "task": "方案发布、供应商分级刷新"},
        {"phase": "Q2", "time": "4-6月", "task": "C/D级帮扶计划启动"},
        {"phase": "Q3", "time": "7-9月", "task": "中期评审与协议补签"},
        {"phase": "Q4", "time": "10-12月", "task": "年度评价与方案复盘"}
    ],
    "pending": [
        "各等级具体PPM红线、准时率目标（按企业实际填入）",
        "审核频次与份额上限的经营阈值",
        "质量协议模板中索赔比例与违约金条款"
    ]
}


def main():
    ap = argparse.ArgumentParser(description="供应商管理方案生成器")
    ap.add_argument("--input", help="结构化方案 JSON 路径（缺省使用内置小样本）")
    ap.add_argument("--out-dir", default=os.getcwd(), help="输出目录（缺省为当前工作目录）")
    ap.add_argument("--format", choices=["txt", "md", "all"], default="all", help="输出格式，默认 all（txt+md）")
    args = ap.parse_args()

    try:
        plan = load_plan(args.input) if args.input else SAMPLE_PLAN
    except Exception as e:
        sys.stderr.write(f"读取输入失败：{e}\n")
        sys.exit(1)

    out_dir = args.out_dir or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)
    date_tag = datetime.now().strftime("%Y%m%d")
    base = f"供应商管理方案_{date_tag}"

    if args.format in ("md", "all"):
        with open(os.path.join(out_dir, base + ".md"), "w", encoding="utf-8") as f:
            f.write(build_md(plan))
        sys.stderr.write(f"MD 已生成：{os.path.join(out_dir, base + '.md')}\n")

    if args.format in ("txt", "all"):
        with open(os.path.join(out_dir, base + ".txt"), "w", encoding="utf-8") as f:
            f.write(build_txt(plan))
        sys.stderr.write(f"TXT 已生成：{os.path.join(out_dir, base + '.txt')}\n")


if __name__ == "__main__":
    main()
