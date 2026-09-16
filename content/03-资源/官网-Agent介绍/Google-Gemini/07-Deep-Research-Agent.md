# Gemini：Deep Research Agent

- **来源**：https://ai.google.dev/gemini-api/docs/deep-research
- **整理日期**：2026-09-16

## 官方要点

1. **自主规划→执行→综合**多步研究，产出带引用的详细报告；支持协作规划、MCP、可视化、文档输入。
2. **仅 Interactions API**（不能走 `generate_content`）；当前 **Preview**。
3. **两个档位**：
   - `deep-research-preview-04-2026`：偏快，适合流式回 UI
   - `deep-research-max-preview-04-2026`：更全面的检索与综合
4. **长任务**：应 `background=true` 异步跑，再轮询/流式取结果（可达数分钟）。
5. **默认工具**：未指定 `tools` 时含 Google Search、URL Context、Code Execution；可显式限制或加 MCP / File Search。
6. **Collaborative planning**：`agent_config.type="deep-research"` + `collaborative_planning=true` 时先出研究计划，用户确认后再继续；设 false/省略可批准执行。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | 研究问题 + 可选协作计划 |
| **工具** | Search / URL / Code / MCP / File Search |
| **循环** | 长时多步 research loop（background） |
| **记忆** | 中间检索与引用汇总进最终报告 |
| **沙箱** | 托管执行；代码执行在 agent 工具侧 |

## 建议精读原文

- https://ai.google.dev/gemini-api/docs/deep-research
- https://ai.google.dev/gemini-api/docs/interactions-overview
