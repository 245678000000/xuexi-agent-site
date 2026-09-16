# OpenAI：Programmatic Tool Calling

- **来源**：https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling
- **整理日期**：2026-09-16

## 官方要点

1. **模型写 JS 编排工具**：在托管 V8 运行时中生成并执行 JavaScript，可并行调用、循环/分支，并把中间结果留在运行时内，最后再把较小的结构化结果交回模型。
2. **适用场景**：可预测的控制流、多结果过滤/聚合/去重；**直接 tool call** 更适合单次查询、每步需要模型再判断、审批敏感写操作、或要保留原生引用/制品的场景。
3. **Responses 配置**：
   - 在 `tools` 中加入 `{"type":"programmatic_tool_calling"}`
   - 对各可调用工具设 `allowed_callers`：`["direct"]` / `["programmatic"]` / 两者皆可
   - 建议为函数同时声明 `parameters` 与 `output_schema`，便于程序可靠读返回字段
4. **支持 programmatic 的工具类型**：function、custom、mcp、apply_patch、local/hosted shell、code_interpreter。MCP 的 `require_approval` 可暂停程序直到批准。
5. **与 Tool Search 组合**：`tool_search` 是顶层工具，**不能**在已运行的 program 内调用；`defer_loading: true` 的工具需先被加载，后续 program 才可通过 `tools.*` 调用。
6. **响应项**：`program`（含 code / call_id / fingerprint）→ 嵌套 `function_call`（`caller` 指向 program）→ `program_output`；应用执行 client-owned 调用后回传 `function_call_output`，**必须原样保留 `caller`**。
7. **Agents API**：默认启用 PTC；可在 `agent.tools` 用 `{"type":"programmatic_tool_calling","enabled":false}` 关闭。`environment.type: none` 的纯会话也可使用；shell/executor MCP 仍需执行环境。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | orchestration 提示划分「代码编排阶段」vs「直接调用阶段」 |
| **工具** | allowed_callers 决定谁能调 |
| **循环** | program 可多次暂停等 client tool 结果 |
| **记忆** | 中间结果可留在 V8，减少塞回模型上下文 |
| **沙箱** | 托管 V8（无 Node/网络/文件系统）；真实副作用仍在各自工具侧 |

## 建议精读原文

- https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling.md
- https://developers.openai.com/api/docs/guides/tools-tool-search.md
- Agents SDK：`ProgrammaticToolCallingTool` / `allowed_callers`
