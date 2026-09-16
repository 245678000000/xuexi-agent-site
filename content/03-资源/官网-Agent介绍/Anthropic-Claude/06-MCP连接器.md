# Anthropic：MCP Connector

- **来源**：https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
- **整理日期**：2026-09-16

## 官方要点

1. **Messages API 直连远程 MCP**：无需自建 MCP client；Anthropic 代为发现/调用远程工具。
2. **Beta**：header `mcp-client-2025-11-20`（旧 `mcp-client-2025-04-04` 已弃用）；**非 ZDR**；Bedrock/Google Cloud 不可用。
3. **两件套**：
   - `mcp_servers[]`：URL、name、OAuth/token
   - `tools[]` 中 `type: "mcp_toolset"`：用 `mcp_server_name` 引用，并可 `default_config` / `configs` 做全开、白名单、黑名单或单工具配置
4. **触发行为**：用户意图映射到工具能力时才调用；「Notion 数据库怎么用」这类通识问题不会乱调工具，「我的 Projects 库里有什么」才会。
5. **限制**：当前主要支持 **tool calls**（非 prompts/resources）；服务器须公网 HTTP（Streamable HTTP / SSE）；**本地 STDIO 不能直连**——本地场景应用自建 MCP client + SDK helpers。
6. **Managed Agents**：创建 agent 时声明最多约 20 个 MCP servers，且每个须被 `mcp_toolset` 引用；可用 vault 凭证（static_bearer / mcp_oauth）。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | 用户请求映射到 MCP 工具描述 |
| **工具** | 远程 MCP tools（服务端代执行） |
| **循环** | API 内部完成 MCP 往返（应用见结果） |
| **记忆** | 工具结果进入消息历史 |
| **沙箱** | 远程服务侧执行；本地 STDIO 需自管 client |

## 建议精读原文

- https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md
- https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers
- https://platform.claude.com/docs/en/managed-agents/mcp-connector
