# Anthropic：Server Tools vs Client Tools

- **来源**：https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- **整理日期**：2026-09-16

## 官方要点

核心分水岭：**代码在哪里执行**。

| 类型 | 谁执行 | 典型例子 | 你要做什么 |
| --- | --- | --- | --- |
| **Client tools** | 你的应用 | 自定义 function、`bash`、`text_editor`、**computer/browser toolset** | 处理 `stop_reason: tool_use`，跑完回 `tool_result` |
| **Server tools** | Anthropic 基础设施 | `web_search`、`web_fetch`、`code_execution`、`tool_search` 等 | 通常直接看到结果，无需本地 handler（与 client 工具同组并行时有例外，见 stop reasons） |

补充：

1. Client 工具是经典 agent 环的「观察→行动→观察」。
2. Server 工具降低集成成本，但可能有**按次用量加价**（如 web search）。
3. Computer / Browser 虽是 Anthropic 定义 schema，但仍属 **client toolset**——截图与点击都在你侧环境。
4. MCP connector 的远程工具更接近「服务端代调远程」，与「你本地执行的 client 工具」不同。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | tool description 决定调用时机 |
| **工具** | client vs server 执行归属 |
| **循环** | client：显式 tool 环；server：平台内嵌 |
| **记忆** | 两类结果都进消息流 |
| **沙箱** | client 工具强依赖你的隔离环境；server 工具在 Anthropic 侧 |

## 建议精读原文

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools
- https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
