# Anthropic：Agent Skills

- **来源**：https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview
- **整理日期**：2026-09-16

## 官方要点

1. **Skills = 文件系统资源包**：把通用 agent 特化为领域专家；相对「一次性 prompt」，可按需加载、跨对话复用。
2. **渐进披露三层**：

| Level | 何时加载 | Token | 内容 |
| --- | --- | --- | --- |
| 1 Metadata | 启动常驻 | ~100/skill | YAML `name`+`description` |
| 2 Instructions | 触发时 | 通常 <5k | SKILL.md 正文 |
| 3+ Resources/code | 按需 | 未读不计 | 参考文档；脚本经 bash 执行，代码本身可不进上下文 |

3. **运行面**：Claude API（container + **必须有 code execution**）、Claude Code（`~/.claude/skills/` 或项目 `.claude/skills/`）、claude.ai（上传 zip）。**跨面不自动同步**。
4. **预置文档 Skills**：pptx / xlsx / docx / pdf（API/云平台/claude.ai；Claude Code 不提供这套预置文档 skill）。
5. **API 约束**：沙箱 **无网络**、不能运行时装包，只能用预装依赖。
6. **安全**：只信自建或 Anthropic 来源；恶意 skill 可诱导调工具/泄密；企业侧可做内容扫描（不等同 API 上传覆盖）。
7. **注意**：Agent Skills **不在 ZDR 覆盖**范围（按标准保留策略）。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | description 触发匹配 |
| **工具** | skill 内 scripts + code execution |
| **循环** | bash 读 SKILL.md → 执行 → 观察输出 |
| **记忆** | 按需读文件，避免全量塞进上下文 |
| **沙箱** | API container / 本地 Claude Code 环境 |

## 建议精读原文

- https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview.md
- https://platform.claude.com/docs/en/build-with-claude/skills-guide
- https://agentskills.io/home（开放标准，跨厂商）
