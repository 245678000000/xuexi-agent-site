# Anthropic：Computer Use

- **来源**：https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool
- **整理日期**：2026-09-16

## 官方要点

1. **客户端工具集**：`{"type":"computer_toolset_20260801"}` 一次声明 ≈ **17 个成员工具**（screenshot、left_click、type、zoom…）；**你的应用在你控制的环境里执行每一次调用**。目前 **不在 Claude Managed Agents** 中提供。
2. **无需 beta header**（新 toolset）；旧版 `computer_20251124` 仍可用但需 beta。
3. **Agent loop**：声明工具 + 用户任务 → Claude 返回带 `toolset_name:"computer"` 的成员 `tool_use` → 按序执行并回 `tool_result` → 重复直到完成。
4. **Batch actions**：一回合可含多步（先点后打后截图）；**必须按顺序执行**，失败后后续块用固定 halt 文案 `Not executed: an earlier computer action in this turn failed.`，且每个 `tool_use` 都要有 `tool_result`（并 echo `toolset_name`）。
5. **坐标**：以你返回的全屏截图像素为准；zoom 不改变坐标系。超限截图需自行缩放。
6. **安全**：隔离 VM/容器、最小权限、敏感凭据勿入环境、互联网 allowlist、高后果动作人审；页面/图像中的指令可能覆盖你的系统提示（prompt injection）。分类器可额外扫描工具返回（可联系支持关闭）。
7. **对比 Browser Use**：纯网页任务优先 browser toolset（读可访问性树/表单/标签页），不必整桌面。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | 用户任务描述（宜具体、分步） |
| **工具** | computer toolset 成员 + 常配 bash/text_editor |
| **循环** | sampling loop / agent loop |
| **记忆** | 截图历史占 token，需修剪/缓存策略 |
| **沙箱** | 客户端自备 VM/Docker 桌面环境 |

## 建议精读原文

- https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool.md
- Browser use：同目录 browser-use-tool
- 参考实现：官方 computer-use reference Docker
