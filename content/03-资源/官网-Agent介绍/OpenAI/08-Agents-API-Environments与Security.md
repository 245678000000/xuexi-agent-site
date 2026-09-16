# OpenAI：Agents API Environments 与 Security

- **来源**：https://developers.openai.com/api/docs/guides/agents-api/environments/security 、https://developers.openai.com/api/docs/guides/agents-api/environments/openai-hosted 、https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted
- **整理日期**：2026-09-16

## 官方要点

### 环境类型

1. **OpenAI-hosted**：`environment.type: openai_hosted`，Linux 工作区（Python/Node/CLI），工作目录 `/workspace`；可配 `packages`、`setup_commands`、`files`、`env`、`skills`/`plugins`/`capability_directories`、`environment_template_id`。
2. **Self-hosted**：自备笔记本/容器/远程沙箱；executor 用环境 ID + 受限 key 经 WebSocket **出站**连接收令回传。
3. **none**：无沙箱会话（仍可用部分不依赖环境的能力，如 PTC）。

### 网络

| `network.access` | 行为 |
| --- | --- |
| `enabled` | 允许出站（默认，除非模板收紧） |
| `disabled` | 阻断出站 |
| `restricted` | 仅 `allowed_domains` 中的精确主机名（1–100，无通配符/协议/路径） |

Hosted **stdio MCP** 目前需要 `enabled`。

### 安全原则（官方）

1. **隔离工作负载**：按用户/租户分环境；应用用独立 OpenAI project。
2. **限制网络**：只放行审批过的端点；Executor MCP 从环境连，Remote MCP 从 OpenAI 服务连。
3. **分离凭证**：
   - 应用 key：`api.agents.read/write`、`api.responses.write`，vault 另需 vault 权限
   - 环境 key 作 `CODEX_API_KEY`：**仅能连环境**，不能干别的 API 动作
   - **应用 API key 绝不进环境**；agent 代码可读到环境 key
4. **第三方凭证走 broker**：尽量不把第三方密钥注入环境；密钥管理器注入仍会暴露给 agent 代码，需轮换/吊销。

### 生命周期要点

- hosted 状态：`provisioning` → `connected`（失败看 `environment.failed`）
- 无活动约 **1 小时**可被删；`/workspace/outputs` 在 turn 完成时发布为不可变 artifact
- 删除 session 触发清理；流关闭不取消任务

## Plugins 说明（本批跳过）

Agents API 有 **Plugins** 文档（打包 skills + MCP 配置复用），与 Codex/插件体系相关。因主题偏「打包分发」且本批已覆盖 Skills/MCP/环境，**本批不单独成文**；batch 4 可按需补。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | session input / agent instructions |
| **工具** | shell / MCP / skills 依赖 environment |
| **循环** | harness 在环境内执行命令与工具 |
| **记忆** | 文件跨 turn 存活；outputs 作 artifact |
| **沙箱** | openai_hosted / self_hosted / none |

## 建议精读原文

- https://developers.openai.com/api/docs/guides/agents-api/environments/security.md
- https://developers.openai.com/api/docs/guides/agents-api/environments/openai-hosted.md
- https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted.md
- https://developers.openai.com/api/docs/guides/agents-api/tools/plugins（batch 4 候选）
