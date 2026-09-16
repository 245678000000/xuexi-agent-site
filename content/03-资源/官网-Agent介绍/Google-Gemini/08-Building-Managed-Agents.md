# Google Gemini：Building Managed Agents（深读）

- **来源**：https://ai.google.dev/gemini-api/docs/custom-agents
- **整理日期**：2026-09-16

## 官方要点（相对既有「Managed/Custom 概览」的加深）

1. **两条路径**：
   - **交互时内联定制** Antigravity：`system_instruction` + `tools` + `environment.sources`（无需先注册）
   - **`agents.create` 持久化**：指定唯一 `id`、`base_agent`、`agent_config`、`system_instruction`、`base_environment`，之后按 ID 调用
2. **文件系统约定**：
   - `.agents/AGENTS.md`（或根级）→ 长篇人设/规范，与 `system_instruction` **叠加**
   - `.agents/skills/<name>/SKILL.md` → Skills，harness 自动发现
3. **创建方式**：
   - **From sources**：每次调用按 sources（inline / Git `repository` / GCS）装新沙箱
   - **Fork 已有 environment**：先交互装好包与文件，再 `base_environment=interaction.environment_id`
   - **Network rules**：创建时可写 allowlist + header `transform` 注入凭证（详见 Environments）
4. **调用与覆盖**：`interactions.create(agent="<id>", ...)`；可覆盖本次的 `system_instruction` / `tools` / `network`（换 token），但 **named agent 的模型在创建时锁定**，交互时不能改 `agent_config.model`。
5. **迭代工作流（官方）**：内联原型 → 稳定环境 → `agents.create` 固化 → 更新定义后下次调用生效。
6. **限制（preview）**：`base_agent` 目前主要是 `antigravity-preview-05-2026`；模型选项含 `gemini-3.8-flash`（默认）等 Flash 系列；无版本回滚；无子 agent 嵌套；最多约 1000 managed agents；`id` 不可用 `google-`/`gemini-`/`antigravity-` 等保留前缀。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | system_instruction + AGENTS.md |
| **工具** | 默认 code_execution/search/url_context + MCP/function |
| **循环** | Interactions API 托管 agent 环 |
| **记忆** | environment 文件持久 + skills |
| **沙箱** | remote environment / fork |

## 建议精读原文

- https://ai.google.dev/gemini-api/docs/custom-agents
- https://ai.google.dev/gemini-api/docs/agent-environment
- https://ai.google.dev/gemini-api/docs/antigravity-agent
