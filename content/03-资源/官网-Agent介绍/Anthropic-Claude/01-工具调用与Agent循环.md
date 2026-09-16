# Anthropic · 工具调用与 Agent 循环（官网导读）

- **来源**：[How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)  
- **整理日期**：2026-09-16  
- **类型**：官方概念页摘要

## 官方最重要的一句话

**Tool use 是你的应用与模型之间的契约。**  
你声明有哪些操作、输入输出长什么样；Claude 决定何时、如何调用。  
**模型从不自己执行任何东西**——它只发出结构化请求；你的代码（或 Anthropic 服务器）执行，再把结果送回对话。

> 学 agent 时把这句话贴在墙上：口才能描述动作，只有工具能真正改世界。

## 工具跑在哪里（三类）

### 1. 用户自定义工具（客户端执行）

你写 schema、你跑代码、你回 `tool_result`。最常见：查库、调内部 API、写文件等。

### 2. Anthropic 预置 schema 工具（仍由客户端执行）

Anthropic 公布 schema，你负责执行。常见：`memory`、`bash`、`text_editor`、`computer`、`browser`。  
好处：模型在这些签名上训练充分，调用更稳、出错恢复更好。

### 3. 服务端执行工具

如 `web_search`、`web_fetch`、`code_execution`、`tool_search`：Anthropic 在服务端跑循环，你通常只需启用工具并读最终结果（少数暂停场景要续跑）。

## Client 侧的 agentic loop（标准形状）

以 `stop_reason` 为条件的 while 循环：

1. 带上 `tools` 和用户消息发请求  
2. 若 `stop_reason == "tool_use"`，取出 `tool_use` 块  
3. 执行工具，打成 `tool_result`  
4. 把助手消息 + 工具结果再发回去  
5. 重复，直到不再是 `tool_use`（如 `end_turn`）

这就是「agent 循环」在 Claude 文档里的工程含义。

## 什么时候该用工具 / 不该用

**该用：** 有副作用的动作；需要新鲜/外部数据；要保证结构化输出；要接到已有系统。

**不该用：** 纯靠训练知识就能答；无副作用的一问一答；工具往返延迟会压过任务本身。

官网提醒：如果你在用正则从模型散文里「抠决定」，这个决定本来就该做成 tool call。

## 建议精读原文

1. [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)  
2. [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)（桌面操控 = 典型 agent loop）  
3. [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
