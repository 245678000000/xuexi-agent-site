# OpenAI：Tool Search

- **来源**：https://developers.openai.com/api/docs/guides/tools-tool-search
- **整理日期**：2026-09-16

## 官方要点

1. **按需加载工具定义**：避免一次性把全部 tool schema 塞进上下文，有助于降 token/成本；新发现的工具注入到上下文**末尾**以尽量保留 prompt cache。
2. **模型门槛（Responses）**：仅 `gpt-5.4` 及更新模型支持 `tool_search`。
3. **启用两步**：
   - `tools` 中加入 `{"type":"tool_search"}`
   - 对要延迟的 function / MCP 设 `defer_loading: true`（namespace 内函数 defer，namespace 对象本身不 defer）
4. **推荐用 namespace / MCP**：模型主要按「命名空间或服务器」的 name+description 搜索；单函数 defer 仍会露出 name/description，主要延迟的是参数 schema。建议每 namespace **&lt;10** 个函数。
5. **两种执行模式**：
   - **Hosted**：候选工具已在请求中声明，API 搜索并同响应返回 `tool_search_call` + `tool_search_output`
   - **Client-executed**：`execution: "client"`，模型发 `tool_search_call`，应用自行检索后回 `tool_search_output`
6. **Agents API**：默认 eager 加载函数；需 defer 时在 `agent.tools` 加 `tool_search` 并对函数设 `defer_loading`。**MCP/plugin 工具**在支持模型上可自动发现，通常不必仅为 MCP 手写 `tool_search`。
7. **注意**：改变已加载工具集会打断 cache；client 模式可返回请求中未预先声明的工具（高级用法，需严格校验）。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | 大工具目录下的任务路由 |
| **工具** | deferred functions / namespaces / MCP |
| **循环** | search → load → function_call |
| **记忆** | 工具加载位置固定在上下文尾部 |
| **沙箱** | Agents API MCP 自动 discovery 依赖会话环境能力 |

## 建议精读原文

- https://developers.openai.com/api/docs/guides/tools-tool-search.md
- https://developers.openai.com/api/docs/guides/function-calling（namespaces）
- https://openai.github.io/openai-agents-python/tools/（ToolSearchTool）
