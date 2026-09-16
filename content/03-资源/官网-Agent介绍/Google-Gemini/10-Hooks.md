# Google Gemini：Agent Hooks

- **来源**：https://ai.google.dev/gemini-api/docs/agent-hooks
- **整理日期**：2026-09-16

## 官方要点

1. **在沙箱内拦截工具前后**：配置发现自 `.agents/hooks.json`（或 `/.agents/hooks.json`），可用 inline / Git / GCS 挂载。
2. **事件**：
   - `pre_tool_execution`：可 `allow` / `deny`（deny 原因回给模型，本 turn 可改道）
   - `post_tool_execution`：审计/格式化/测报；**不能**撤销已发生动作
3. **Handler 类型**：
   - `command`：沙箱内跑脚本，stdin JSON → stdout 决策
   - `http`：POST 到外部 HTTPS；须在 `network.allowlist`；凭据用 egress `transform` 注入，勿写进 hooks.json
4. **Matcher**：RE2 正则匹配容器内工具名，如 `code_execution`、`read_file|write_file`、`.*_file`、`*` 全匹配。
5. **失败默认放行**：脚本崩溃、非 2xx、超时、无法识别 JSON → 视为 `allow`，避免死锁。
6. **范围限制**：只拦沙箱内置 `code_execution` 与 filesystem（`read_file`/`write_file`/`list_files`/`delete_file`）；**不拦**外部 `function` 与 `mcp_server`。
7. **篡改风险**：有写文件/shell 权限的 agent 可能改 hooks；严格场景应用只读源或额外策略。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | 策略/合规规则编码进 hooks |
| **工具** | 被 matcher 命中的沙箱工具 |
| **循环** | 同步等待 hook → 再执行/跳过 |
| **记忆** | 多 turn 可复用同 environment 继续 |
| **沙箱** | hooks 跑在 sandbox 网络命名空间 |

## 建议精读原文

- https://ai.google.dev/gemini-api/docs/agent-hooks
- 与 Anthropic Managed Agents `permission_policy` / OpenAI guardrails 对照见跨厂商笔记
