# Anthropic：Managed Agents 工具与权限

- **来源**：https://platform.claude.com/docs/en/managed-agents/tools 、https://platform.claude.com/docs/en/managed-agents/permission-policies
- **整理日期**：2026-09-16

## 官方要点

### 内置 agent toolset（`agent_toolset_20260401`）

| 工具 | name |
| --- | --- |
| Bash | `bash` |
| Read / Write / Edit | `read` / `write` / `edit` |
| Glob / Grep | `glob` / `grep` |
| Web fetch / search | `web_fetch` / `web_search` |

- 默认全部启用；`configs` 可关单项；`default_config.enabled: false` + 白名单可「只开需要的」。
- 超长工具输出（&gt;约 10 万字符）自动落沙箱文件，模型拿预览路径再读。
- `web_search`/`web_fetch`：**在 Anthropic 服务器执行**，不受环境 `networking` 约束；用各自 `allowed_domains` 或 `blocked_domains`（不可同条目两者都设）限制。组织级 Console 网页设置**不**作用于 Managed Agents。

### 权限策略（仅 server 侧工具：agent toolset + MCP）

| Policy | 行为 |
| --- | --- |
| `always_allow` | 自动执行（**agent toolset 默认**） |
| `always_ask` | 会话暂停，等人确认（**MCP toolset 默认**） |
| `auto` | 服务端逐次评估：放行 / 拒绝 / 转人工 |

- 自定义工具**不受** permission policy 约束（应用收到 `agent.custom_tool_use` 自行决定）。
- `always_ask`/`auto`→ask：发 `user.tool_confirmation`（`allow`/`deny` + 可选 `deny_message`）。
- 事件带 `evaluated_permission` 与 `evaluation`（可审计 `reason_code` 如 `high_risk`）。
- **`auto` 不是人审替代**：判定安全会直接跑；关键工具仍应用 `always_ask`。

### MCP 工具集

- agent 声明 `mcp_servers` + 匹配的 `mcp_toolset`；可对 MCP 工具做 enabled 白/黑名单与 permission_policy。
- 会话用 `vault_ids` 注入凭证（URL 匹配）；连接失败不阻止开会话，会发 `session.error`。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | agent.system + session 用户消息 |
| **工具** | agent_toolset / mcp_toolset / custom |
| **循环** | session event stream + confirmation |
| **记忆** | 沙箱文件 / memory stores（另文） |
| **沙箱** | cloud / self-hosted environments |

## 建议精读原文

- https://platform.claude.com/docs/en/managed-agents/tools.md
- https://platform.claude.com/docs/en/managed-agents/permission-policies.md
- https://platform.claude.com/docs/en/managed-agents/mcp-connector.md
