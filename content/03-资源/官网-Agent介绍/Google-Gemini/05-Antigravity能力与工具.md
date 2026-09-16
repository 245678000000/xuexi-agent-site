# Gemini：Antigravity Agent 能力与工具

- **来源**：https://ai.google.dev/gemini-api/docs/antigravity-agent
- **整理日期**：2026-09-16

## 官方要点

1. **定位**：Gemini API 上的通用托管 agent；单次调用即可在 Google 托管 Linux sandbox 中推理与行动；与 Antigravity IDE **同一 harness**。
2. **调用入口**：Interactions API；agent id 例：`antigravity-preview-05-2026`；常设 `environment="remote"`。
3. **默认工具**（未传 `tools` 时）：`code_execution`、`google_search`、`url_context`；指定 `environment` 后自动启用 **Filesystem**。
4. **工具表（摘要）**：

| 能力 | type | 说明 |
| --- | --- | --- |
| Code execution | `code_execution` | bash/python 等命令，stdout/stderr |
| Google Search | `google_search` | 公网搜索 |
| URL Context | `url_context` | 抓取阅读网页 |
| Filesystem | （environment 启用） | 读写改搜列目录 |
| Custom Functions | `function` | 自定义 API |
| Remote MCP | `mcp_server` | 注册外部 MCP |

5. **Hooks**：可在 remote sandbox 内对 `code_execution` / filesystem **同步拦截校验**。
6. **模型**：默认 Gemini 3.8 Flash（`gemini-3.8-flash`）；可用 `agent_config` 换模型优化速度/成本/推理。
7. Preview：Studio + Gemini API，免费/付费层均有（以官网为准）。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | `input` 任务描述 |
| **工具** | 上表默认集 + 自定义/MCP |
| **循环** | 托管 agent loop 直至任务完成 |
| **记忆** | 沙箱文件即工作记忆；交互可串联 |
| **沙箱** | `environment=remote` 托管 Linux |

## 建议精读原文

- https://ai.google.dev/gemini-api/docs/antigravity-agent
- https://ai.google.dev/gemini-api/docs/interactions-overview
