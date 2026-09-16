# Google Gemini：Managed Agents Environments

- **来源**：https://ai.google.dev/gemini-api/docs/agent-environment
- **整理日期**：2026-09-16

## 官方要点

1. **环境 = 托管 Linux 沙箱**，与对话上下文解耦：可跨多次 interaction 复用，也可每次新建。
2. **`environment` 三种写法**：
   - `"remote"`：全新沙箱
   - `"env_…"`：复用已有 ID（保留文件与已装包）
   - `{type, sources, network, …}`：声明式配置

3. **Sources**：

| type | 说明 | 限额 |
| --- | --- | --- |
| `repository` | Git clone 到 target | 500 MB |
| `gcs` | 从 Cloud Storage 拷贝 | 2 GB |
| `inline` | 写文本文件 | 单文件 1 MB / 合计 2 MB |

不可把 `target` 设为根 `/`。

4. **网络**：默认开放出站；`network.allowlist` 按域名放行，可选 `transform` 在**出口代理**注入 Authorization 等头（**密钥不落沙箱环境变量/文件**）；`network: "disabled"` 全禁。可在同 `environment_id` 上刷新 network 规则以轮换 token。
5. **生命周期**：创建 → Active → Idle（约 15 分钟无活动快照停机）→ Offline（自上次活跃起约 **7 天**可恢复）→ Deleted。
6. **资源**：约 4 vCPU / 16 GB；preview 期环境算力不单独计费。预装 Ubuntu + Python 3.12/Node 22 等常用包。
7. **API**：`environments.list/get/delete`；可用 Files API 下载 `environment-<id>` 快照 tar。
8. **Hooks**：可挂 `.agents/hooks.json`（见 Hooks 专文）。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | interaction input |
| **工具** | 沙箱内 code_execution / filesystem；MCP 在容器外 |
| **循环** | previous_interaction_id + environment_id |
| **记忆** | 文件系统跨 turn；TTL 7 天 |
| **沙箱** | remote managed Linux |

## 建议精读原文

- https://ai.google.dev/gemini-api/docs/agent-environment
- https://ai.google.dev/gemini-api/docs/agent-hooks
