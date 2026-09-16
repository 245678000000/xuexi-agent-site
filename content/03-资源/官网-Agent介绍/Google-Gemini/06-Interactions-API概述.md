# Gemini：Interactions API 概述

- **来源**：https://ai.google.dev/gemini-api/docs/interactions-overview
- **整理日期**：2026-09-16

## 官方要点

1. **2026-06 起 GA**，推荐新项目统一用 Interactions；`generateContent` 仍支持但标为 legacy。
2. **一个接口同时服务**：普通 Gemini 模型调用 + 专用 agents（Deep Research、Antigravity、custom managed agents）。
3. 覆盖能力示例：文本/图像/音视频理解、function calling、structured output、Deep Research、Flex/Priority inference 等。
4. **混合编排**：可用 `previous_interaction_id` 把「Research agent 收集」与「普通模型总结」串在同一对话链。
5. Agent id 示例（以文档当时为准）：
   - `deep-research-preview-04-2026` / `deep-research-max-preview-04-2026`
   - `antigravity-preview-05-2026`

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | interaction `input` |
| **工具** | 模型 tools 或 agent 内置工具 |
| **循环** | 单次 interaction 内可多步；长任务可 background |
| **记忆** | `previous_interaction_id` |
| **沙箱** | agent+environment 时由托管侧提供 |

## 建议精读原文

- https://ai.google.dev/gemini-api/docs/interactions-overview
- https://ai.google.dev/api/interactions-api（参考）
- Migrate to Interactions API（迁移注意）
