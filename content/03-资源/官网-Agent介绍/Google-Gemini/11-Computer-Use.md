# Google Gemini：Computer Use

- **来源**：https://ai.google.dev/gemini-api/docs/computer-use
- **整理日期**：2026-09-16

## 官方要点

1. **客户端 UI 自动化工具**：模型看截图，产出点击/键盘等 `function_call`；**执行环境与 Playwright 等由你实现**。走 Interactions API，例如 `tools: [{"type":"computer_use","environment":"browser"}]`。
2. **环境（Gemini 3.x）**：`browser` / `mobile` / `desktop`（文档亦写 ENVIRONMENT_* 枚举）；动作集不同（浏览器含 navigate/go_back；移动含 open_app/list_apps/long_press 等）。
3. **Agent 环**：发截图+提示 → 收 action（3.x 常带 `intent` 解释）→ 客户端缩放坐标（归一化 0–1000）并执行 → 回传 `function_result`（含新截图）→ 重复。
4. **安全**：
   - 内置策略类别（金融交易、敏感数据、发消息、开户、同意条款等）可触发 `require_confirmation`
   - `disabled_safety_policies` 可覆盖部分策略偏好，但应用仍须处理 `safety_decision`
   - `enable_prompt_injection_detection`（默认 false）扫描截图中的对抗指令
5. **与 Antigravity managed agent**：Antigravity 文档明确 **`computer_use` 尚不在其托管工具列表**；Computer Use 是 Interactions 上面向模型的独立工具能力。
6. **Preview 警告**：官方要求敏感/不可逆任务保持人审，沙箱隔离，日志与 allow/blocklist。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | 用户自然语言任务 |
| **工具** | computer_use 预定义动作 + 可选自定义 function |
| **循环** | Interactions 多 turn + previous_interaction_id |
| **记忆** | 截图历史在对话中；需自行管理长度 |
| **沙箱** | 应用侧 VM/Docker/浏览器配置文件 |

## 建议精读原文

- https://ai.google.dev/gemini-api/docs/computer-use
- 对比 Anthropic Browser Use / Computer Use；OpenAI Computer Use（若库中已有）
