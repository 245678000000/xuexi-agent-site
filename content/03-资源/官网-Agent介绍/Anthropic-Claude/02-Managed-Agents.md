# Anthropic · Claude Managed Agents（官网导读）

- **来源**：[Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)  
- **整理日期**：2026-09-16  
- **类型**：官方概念页摘要  
- **状态提示**：文档称需 beta header（如 `managed-agents-2026-04-01`），以官网最新为准

## 和 Messages API 的差别

| | Messages API | Claude Managed Agents |
|--|--------------|------------------------|
| 是什么 | 直接提示模型 | 预构建、可配置的 agent harness，跑在托管基础设施上 |
| 适合 | 自定义 agent 循环、要细粒度控制 | 长任务、异步工作 |

你不必自己搭：agent loop、工具执行、运行时；Claude 可在托管环境里读文件、跑命令、上网、跑代码。Harness 还带 prompt caching、compaction 等优化。

## 四个核心概念

| 概念 | 含义 |
|------|------|
| **Agent** | 模型 + system prompt + tools + MCP + skills |
| **Environment** | 会话跑在哪：Anthropic 云沙箱，或自托管沙箱 |
| **Session** | 在某个环境里跑着的 agent 实例，执行具体任务并产出 |
| **Events** | 应用与 agent 之间的消息（用户轮次、工具结果、状态更新） |

## 适合什么工作负载

- 需要跑很多分钟、多次工具调用的长任务  
- 要安全沙箱 / 预装环境  
- 合规需要自托管执行环境  
- 不想自建 loop / 沙箱 / 工具层  
- 需要跨多轮保留文件系统与对话状态  
- 需要按 cron 调度的定期运行  

## 建议精读原文

1. [Overview](https://platform.claude.com/docs/en/managed-agents/overview)  
2. [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)  
3. [Define your agent](https://platform.claude.com/docs/en/managed-agents/agent-setup)
