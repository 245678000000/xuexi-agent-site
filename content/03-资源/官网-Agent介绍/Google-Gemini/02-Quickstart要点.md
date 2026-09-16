# Google Gemini · Managed Agents Quickstart 要点

- **来源**：[Managed agents quickstart](https://ai.google.dev/gemini-api/docs/managed-agents-quickstart)  
- **整理日期**：2026-09-16

## 最小调用在做什么

一次 `interactions.create` 大致做三件事：

1. 指定 `agent`（如文档中的 Antigravity 预览版 ID）  
2. `environment="remote"`：新开干净沙箱  
3. `input`：你要它完成的目标  

返回里记住：

- `interaction.id` —— 对话上下文续跑  
- `environment_id` —— 沙箱/文件状态续跑  
- `output_text` —— 最终回答  
- `steps` —— 推理 / 工具 / 跑代码等步骤轨迹（拆解学习超有用）

## 两套状态要分清

| 维度 | 用什么续 | 存的是什么 |
|------|----------|------------|
| 对话上下文 | `previous_interaction_id` | 聊天、推理轨迹、工具使用 |
| 环境状态 | `environment` / environment id | 文件、已装包、沙箱磁盘 |

可混用：清对话但留文件；留对话但换新沙箱。

## 长对话

文档提到约在 135k tokens 量级会做 **context compaction**，减轻上下文腐烂与爆窗。

## 进阶

- 流式看 agent 实时干活  
- 从 environment 下载产物（tar snapshot）  
- `agents.create` 把 instructions / skills / 模型 / 环境固化成可复用 managed agent，之后按 ID 调用
