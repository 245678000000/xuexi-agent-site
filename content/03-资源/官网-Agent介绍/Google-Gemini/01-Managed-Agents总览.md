# Google Gemini · Managed Agents 总览（官网导读）

- **来源**：[Agents overview](https://ai.google.dev/gemini-api/docs/agents)  
- **整理日期**：2026-09-16  
- **类型**：官方概念页摘要  
- **状态**：Public Preview（以官网为准）

## 官方一句话

Gemini API 上的 **Managed agents** 给你一个可配置的 **agent harness**。  
一次 API 调用即可拉起 **Linux 沙箱**：agent 在里面推理、执行代码、管理文件、浏览网页。

## 现成托管 Agent（文档列出）

- **Antigravity agent**：通用托管 agent；在 Google 托管的安全 Linux 沙箱里跑代码、管文件、搜网页。可用 `agent_config` 换底层模型，并叠加自己的 instructions / skills / 数据做成定制 agent。  
- **Deep Research**：自主调研类 agent，规划—执行—综合多步研究（市场分析、尽调、文献综述等场景）。

另有 **AI Studio** 可视化 playground，可先不写代码做原型。

## 安全与使用注意（官网强调）

- Preview：敏感工作流上线前务必审查动作与输出  
- 默认沙箱 OS 级隔离；默认出站网络较开放，可用 allowlist 收紧  
- 外接工具 / API：最小权限、短时令牌、定期轮换；凭证不要暴露进沙箱  
- **人审**：生成代码、改数据、碰外部系统前先核对  

## 计费与限制（摘要）

- 按模型 token + 工具用量计费；一次 interaction 可能触发多轮推理，文档称常见约 100k–3M tokens  
- Preview 期间环境算力可能不单独计费（以定价页为准）  
- 环境闲置约 7 天会永久删除；VM 短暂闲置会休眠，下次请求冷启动恢复  
- 预装环境基于 Ubuntu，含 Python 3.12、Node.js 22 等  

## 也可用框架自建

官网列出：LangChain/LangGraph、LlamaIndex、CrewAI、Vercel AI SDK、**Google ADK**、**Antigravity SDK** 等。

## 建议精读原文

1. [Agents overview](https://ai.google.dev/gemini-api/docs/agents)  
2. [Managed agents quickstart](https://ai.google.dev/gemini-api/docs/managed-agents-quickstart)  
3. [Building managed agents](https://ai.google.dev/gemini-api/docs/custom-agents)  
4. [Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview)
