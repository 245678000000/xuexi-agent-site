# OpenAI · Agents 总览（官网导读）

- **来源**：[Agents | OpenAI API](https://developers.openai.com/api/docs/guides/agents)  
- **整理日期**：2026-09-16  
- **类型**：官方概念页摘要（非全文转载）

## 官方一句话

Agents 可以**规划并用工具完成任务**，可以和其他 agent 协作，并在多步之间保持上下文。先选 runtime：编排跑在哪、状态谁管。

## 你该从哪条路开始

| 你想要… | 官方建议入口 |
|---------|--------------|
| OpenAI 托管 Codex harness，长任务、进度由平台保存 | **Agents API** |
| 在自己应用里控制循环，可复用 agents / tools / handoffs | **Agents SDK** |
| 直接跟模型响应打交道，或从零搭 agent | **Responses API** |
| 嵌入式聊天体验 | **ChatKit** |

## 三条运行时怎么选（官网对比要点）

| | Agents API | Agents SDK | Responses API |
|--|------------|------------|---------------|
| 适合 | 长任务，OpenAI 管 agent 并保存进度 | 自定义工具与工作流 | 直接调模型 / 从零构建 |
| Agent 跑在哪 | OpenAI 托管的 Codex harness | 你的应用进程内 | 你的应用（可选托管编排） |
| 接入成本 | 低 | 中 | 高 |
| 任务间状态 | 会话配置、turns、items 由平台保存 | 你自己存，或 SDK session / Responses 会话 | 手动历史、response 链式、Conversations |
| 工具执行 | 服务侧工具 + 应用函数处理 + 可选沙箱 | 你在应用里配置的工具 | 托管工具 + 你本地跑的工具 |

## 贯穿能力

无论走哪条路，官网都强调再学这些：

- **Tools**：函数调用、MCP、托管能力 —— [Using tools](https://developers.openai.com/api/docs/guides/tools)
- **Skills**：可复用指令包 —— [Skills](https://developers.openai.com/api/docs/guides/tools-skills)
- **Prompt caching**：降低重复前缀成本 —— [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)

注意：Agents API session、SDK session、Responses conversation、sandbox 是**不同资源**，清理与状态规则不能混用。

## 建议精读原文

1. [Agents 总览](https://developers.openai.com/api/docs/guides/agents)（本页）  
2. [Agents SDK Quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart)  
3. [Agents API overview](https://developers.openai.com/api/docs/guides/agents-api/overview)（若关心托管长任务）

## 和你学习目标的对应

- 「Agent ≠ 聊天」：这里体现在 **tools + multi-step + state**  
- 「循环谁来转」：Agents API / Managed 类产品帮你转；SDK / Responses 要你自己转（或部分自己转）
