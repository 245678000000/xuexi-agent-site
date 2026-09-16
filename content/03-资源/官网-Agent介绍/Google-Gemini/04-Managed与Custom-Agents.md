# Gemini：Managed Agents / Custom Agents

- **来源**：https://ai.google.dev/gemini-api/docs/agents
- **整理日期**：2026-09-16

## 官方要点

1. **Managed agents**：一次 API 调用配置 agent harness；Google 托管 **Linux sandbox**，agent 自主推理、跑代码、管文件、浏览网页。
2. 主线产品：
   - **Antigravity**：通用托管 agent（同 Antigravity IDE harness）
   - **Deep Research**：多步研究并生成带引用报告
3. **Custom / managed agent 构建**：可通过 `agents.create` 固化 instructions、tools、model；之后 interaction 时模型锁定，保证工具行为与安全边界可预期。
4. 配额提示：文档提及可创建大量 managed agents（量级约千级，以官网最新为准）。
5. 计费：按 Gemini token + 工具用量；preview 期 environment compute 可能不计费（以定价页为准）；免费层有额度。
6. 生态旁路：LangGraph / CrewAI / ADK / Antigravity SDK 等用于自建编排，不等于托管 sandbox 同路径。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | agent instructions / 用户 input |
| **工具** | 内置工具 + 自定义 function + MCP |
| **循环** | 托管 sandbox 内 reason→act→observe |
| **记忆** | Interactions 可 `previous_interaction_id` 串联 |
| **沙箱** | Google 托管 Linux environment |

## 建议精读原文

- https://ai.google.dev/gemini-api/docs/agents
- https://ai.google.dev/gemini-api/docs/antigravity-agent（能力细节）
- Building managed agents / Environments / Hooks（同站点 Agents 目录）
