# 跨厂商：MCP 对照（OpenAI / Anthropic / Gemini）

- **来源**：
  - OpenAI Agents API：https://developers.openai.com/api/docs/guides/agents-api/tools/mcp
  - Anthropic Messages MCP connector + Managed Agents：https://platform.claude.com/docs/en/agents-and-tools/mcp-connector 、https://platform.claude.com/docs/en/managed-agents/mcp-connector
  - Gemini Antigravity：https://ai.google.dev/gemini-api/docs/antigravity-agent（MCP servers 节）
- **整理日期**：2026-09-16

## 一句话

三家都能把 **远程 MCP** 接到 agent；差异主要在 **连接原点（谁连服务器）**、**鉴权与密钥存放**、**权限/审批默认值**、以及 **stdio/本地进程**是否一等公民。

## 对照表

| 维度 | OpenAI（Agents API） | Anthropic | Gemini（Antigravity） |
| --- | --- | --- | --- |
| 声明位置 | `agent.tools[]` type `mcp` | Messages：`mcp_servers` + `mcp_toolset`；Managed：agent 上 servers + toolset，session `vault_ids` | `tools[]` type `mcp_server`（name/url/headers/allowed_tools） |
| 传输 | HTTP（service 或 environment）+ **stdio**（环境内起进程） | 远程 HTTP（Streamable HTTP/SSE）；本地 STDIO 需自建 client | 远程 **Streamable HTTP**；文档称 **不支持 SSE** |
| 连接原点 | `connection_origin: service`（OpenAI）或 `environment`（会话沙箱） | 平台代连公网远程服务器 | 平台侧连远程 URL |
| 鉴权 | 会话内联 authorization/headers；或 vault（仅 service 原点）；stdio 用 env_vars | Managed：vault（static_bearer / mcp_oauth）按 URL 匹配；Messages：OAuth/token 配在 server | `headers` 自定义；可配合环境网络 transform |
| 工具过滤 | `allowed_tools` | `mcp_toolset` default_config/configs enabled | `allowed_tools`（省略则全开） |
| 审批默认 | 可配置 require_approval 等 | Managed MCP 默认 `always_ask` | 无同等 permission_policy；沙箱 hooks **不**拦截 MCP |
| 规模/发现 | 可与 Tool Search 自动发现 MCP（支持模型） | agent 最多约 20 servers；须 toolset 一一引用 | name 须小写字母数字/`_`/`-` |
| 失败行为 | `required: true` 可令 turn 失败 | 会话仍可开，发 `session.error`（连接/鉴权失败） | 按交互错误处理（见 API） |

## 选型提示

1. **私网 MCP**：OpenAI `connection_origin: environment` 或 stdio；Anthropic/Gemini 远程模式需公网或自建桥。
2. **密钥**：OpenAI/Anthropic 都推 vault +「密钥不进 agent 可读环境」；Gemini 用 egress header transform 同类思路。
3. **人审**：Anthropic Managed 对 MCP 默认询问；OpenAI/Gemini 需自行叠审批或产品层确认。

## 建议精读原文

- 上表三家链接的 `.md` 版（OpenAI/Anthropic 支持 URL.md）
- OpenAI Tool Search Agents API 节（MCP 自动 discovery）
