# Anthropic：Browser Use

- **来源**：https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool
- **整理日期**：2026-09-16

## 官方要点

1. **客户端浏览器工具集**：`tools` 中加 `{"type":"browser_toolset_20260801"}`（无 `name`），默认约 27 个成员工具，另有 4 个可选（`javascript_exec` / `file_upload` / `read_console` / `read_network`，默认关）。
2. **与 Computer Use 区别**：Browser Use 同时用 **无障碍树/元素引用** 与截图坐标；Computer Use 主要是整桌面截图+坐标。页面内任务优先 Browser；整桌面用 Computer Use；只读公开页可用更轻的 server 工具 `web_fetch` / `web_search`。
3. **执行方**：全部由**你的应用**驱动本地浏览器自动化；Anthropic 侧不跑浏览器。**目前不可用于 Claude Managed Agents**。
4. **平台**：Claude API 与 Google Cloud；不在 AWS Claude Platform / Bedrock / Microsoft Foundry。
5. **循环**：`stop_reason: tool_use` → 多个带 `toolset_name: "browser"` 的成员调用 → **按顺序**执行（batch，失败后后续用固定文案 `Not executed: an earlier action in this turn failed.`）→ 回传 `tool_result`（须回显 `toolset_name`）。
6. **目标定位**：`RefTarget`（`read_page`/`find` 产出的 `[ref_n]`）优先；无障碍树不足时回退坐标。Tab 状态用 `browser_state` 块上报。
7. **安全**：隔离浏览器/凭证、域名 allowlist、拒绝非 http(s)、页面内容视为不可信输入、人审关键操作；可选开启注入分类器。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | 用户提示驱动网页任务 |
| **工具** | browser toolset 成员（navigate/read_page/click…） |
| **循环** | Messages API tool_use 环 + 批动作顺序执行 |
| **记忆** | tab/ref 状态在应用侧；结果进对话 |
| **沙箱** | 应用自管浏览器容器/VM |

## 建议精读原文

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool.md
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-combinations
- Computer Use 对照：同目录 computer-use 文档
