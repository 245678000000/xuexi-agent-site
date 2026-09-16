# OpenAI：工具 / Function Calling / MCP

- **来源**：https://developers.openai.com/api/docs/guides/tools 、https://developers.openai.com/api/docs/guides/function-calling 、https://developers.openai.com/api/docs/guides/agents-api/tools/mcp
- **整理日期**：2026-09-16

## 官方要点

1. **工具是能力扩展层**：Responses / Agents API / Agents SDK 三条集成路径语义一致，但接线位置不同（请求参数 vs `agent.tools` vs Agent 定义）。
2. **Function calling 五步环**：声明 tools → 模型产出 tool call → 应用侧执行 → 回传 tool output → 继续对话（可多轮）。
3. **工具类型分层**：
   - Function（JSON Schema）
   - Custom（自由文本输入，可挂 grammar）
   - Built-in（web_search、file_search、shell、computer use、MCP 等）
4. **MCP（Agents API）**：MCP server 发布工具定义并执行调用；Agents API 负责发现与调用，应用可不手工处理每次 call。
5. **连接原点**决定谁连服务器：

| Connection | 运行位置 | 需要 environment |
| --- | --- | --- |
| HTTP `connection_origin: "service"`（默认） | OpenAI | 否 |
| HTTP `connection_origin: "environment"` | 会话环境 | 是 |
| stdio | 会话环境内进程 | 是 |

6. **大规模工具面**：`tool_search` + `defer_loading`（约 gpt-5.4+）按需加载，避免一开始塞满上下文。
7. **Strict mode**：`strict: true` 用结构化输出约束参数；要求 `additionalProperties: false` 且 properties 全在 required（可选字段用 `["string","null"]`）。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | `input` / instructions 决定何时调工具 |
| **工具** | function / built-in / MCP / custom |
| **循环** | Responses 多轮 tool 环；Agents API 由 harness 托管 |
| **记忆** | 工具结果进会话上下文；Sessions 保留状态 |
| **沙箱** | MCP environment / shell / hosted sandbox |

## 建议精读原文

- https://developers.openai.com/api/docs/guides/tools.md
- https://developers.openai.com/api/docs/guides/function-calling.md
- https://developers.openai.com/api/docs/guides/agents-api/tools/mcp.md
- https://developers.openai.com/api/docs/guides/tools-connectors-mcp（Responses 侧 Remote MCP）
