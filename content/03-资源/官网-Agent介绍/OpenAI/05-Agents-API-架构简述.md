# OpenAI Agents API：架构简述

- **来源**：https://developers.openai.com/api/docs/guides/agents-api/overview
- **整理日期**：2026-09-16

## 官方要点

1. **定位**：通过 OpenAI 托管 API 使用 **Codex harness**；OpenAI 管 session、编排、上下文压缩与恢复；应用提供 tools 并选择执行环境。
2. **四大概念**：

| 概念 | 含义 |
| --- | --- |
| **Agent** | 模型、instructions、tools、MCP |
| **Environment** | 可选 sandbox/computer：文件、skills、命令 |
| **Session** | Agent 的持久实例，承接任务与输入 |
| **Events / items** | 输入与会话中产出的输出事件 |

3. **典型流程**：创建 session（配置 agent，可托管环境）→ 给任务 → 流式/webhook 跟进 → continue/steer。
4. **Harness 能力**：沙箱跑命令、加载 skills、MCP/工具、运行中转向、上下文摘要、子任务/subagents、会话续跑。
5. **计费**：模型 API 价 + 内置工具价 + hosted sandbox container 价；数据驻留目前偏美国；**不支持 ZDR**（自建 sandbox 也不使 Agents API 变成 ZDR）。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | session input / instructions |
| **工具** | `agent.tools`（含 MCP、PTC、web_search…） |
| **循环** | 托管 agent loop（应用收事件） |
| **记忆** | session 保留跨轮状态 |
| **沙箱** | openai_hosted / self_hosted environment |

## 建议精读原文

- https://developers.openai.com/api/docs/guides/agents-api/overview.md
- https://developers.openai.com/api/docs/guides/agents-api/quickstart
- https://developers.openai.com/api/docs/guides/agents#compare-agent-runtimes
