# Anthropic：Memory Tool

- **来源**：https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- **整理日期**：2026-09-16

## 官方要点

1. **跨会话持久记忆（客户端）**：工具类型 `memory_20250818`，`name` 必须为 `memory`；Claude 发出文件操作请求，**你的应用**对 `/memories` 前缀映射的真实存储执行并回 `tool_result`。
2. **Just-in-time**：不把全部记忆塞进上下文；先 `view` 目录再按需读文件，适合长会话。
3. **命令集**：`view` / `create` / `str_replace` / `insert` / `delete` / `rename`（官方约定推荐返回文案与错误格式）。
4. **自动系统提示片段**：启用后 API 会注入「先查看 memory 目录再开工、随时可能被打断所以要写回 memory」一类协议。
5. **SDK helpers**：Python/TS 等提供 `BetaLocalFilesystemMemoryTool` / `betaMemoryTool` 与 tool runner；Go/Ruby 需自写循环。
6. **安全**：路径穿越防护（强制 `/memories`、canonicalize、拒 `../`）；敏感信息校验；文件大小/过期策略；按用户隔离存储。
7. **与 Managed Agents**：Messages API 的 memory tool 是 client schema；Managed Agents 另有 **memory stores / Using agent memory**（workspace 记忆，beta header 不同）。二者勿混为一谈。
8. **搭配**：可与 context editing、server compaction 同用——compaction 压缩对话，memory 保留必须跨摘要存活的事实。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | 任务前先读 memory 协议 |
| **工具** | 单一 `memory` 命令工具 |
| **循环** | 标准 tool_use 环 |
| **记忆** | `/memories` 文件树（应用侧持久化） |
| **沙箱** | 存储完全由应用控制 |

## 建议精读原文

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool.md
- Managed Agents：https://platform.claude.com/docs/en/managed-agents/memory
- Context editing / Compaction 相关文档
