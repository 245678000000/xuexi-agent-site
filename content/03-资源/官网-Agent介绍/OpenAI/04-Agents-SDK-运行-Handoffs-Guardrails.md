# OpenAI Agents SDK：运行 / Handoffs / Guardrails

- **来源**：https://developers.openai.com/api/docs/guides/agents/orchestration 、https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
- **整理日期**：2026-09-16

## 官方要点

### Orchestration：两种所有权模型

| Pattern | 何时用 | 发生什么 |
| --- | --- | --- |
| **Handoffs** | 专科应接管该分支的用户可见回复 | 控制权交给专科 Agent |
| **Agents as tools** | Manager 应保持对外回复，专科只做有界能力 | Manager 保留回复所有权 |

- 先能单 Agent 就别拆；只有指令/工具/策略真的分叉时再拆专科。
- Handoff 描述保持短而具体；asTool 适合摘要/分类等有界任务。

### Guardrails vs Human review

| 场景 | 起点 |
| --- | --- |
| 主模型跑之前拦截违规请求 | Input guardrails |
| 最终输出离开系统前校验/脱敏 | Output guardrails |
| 函数工具参数/结果检查 | Tool guardrails |
| 取消、编辑、shell、敏感 MCP 等副作用前暂停 | Human-in-the-loop approvals |

- Input guardrail 可阻塞（`runInParallel: false`）或并行（更低延迟）。
- Approval 生命周期：中断 → `interruptions` + resumable `state` → approve/reject → 从同一 `state` 恢复（可序列化后延迟审批）。
- **边界提醒**：input guardrail 只对链路第一个 agent；output 只对产出最终输出的 agent；不要指望 agent 级 guardrail 覆盖所有嵌套工具副作用。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | Triage/manager instructions 决定路由 |
| **工具** | 专科 asTool；敏感工具 `needsApproval` |
| **循环** | Runner.run → interruption → resume |
| **记忆** | `state` / `lastAgent` 跨轮续跑 |
| **沙箱** | shell/MCP 副作用应落在审批边界外 |

## 建议精读原文

- https://developers.openai.com/api/docs/guides/agents/orchestration.md
- https://developers.openai.com/api/docs/guides/agents/guardrails-approvals.md
- https://developers.openai.com/api/docs/guides/agents/running-agents
