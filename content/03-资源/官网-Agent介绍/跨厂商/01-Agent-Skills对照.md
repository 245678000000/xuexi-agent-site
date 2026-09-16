# 跨厂商：Agent Skills 对照（OpenAI / Anthropic / Gemini）

- **来源**：
  - OpenAI：https://developers.openai.com/api/docs/guides/tools-skills
  - Anthropic：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - Gemini：https://ai.google.dev/gemini-api/docs/custom-agents（`.agents/skills/**/SKILL.md`）
  - 开放标准：https://agentskills.io/home
- **整理日期**：2026-09-16

## 一句话

三家都走向 **「目录 + SKILL.md（YAML front matter + 指令）+ 按需加载」**；OpenAI/Anthropic 明确对接开放 Agent Skills 规范，Gemini 在 Antigravity 环境里用同构文件约定自动发现。

## 对照表

| 维度 | OpenAI | Anthropic | Gemini |
| --- | --- | --- | --- |
| 核心文件 | `SKILL.md` | `SKILL.md` | `SKILL.md` |
| 发现元数据 | name + description（进 user prompt） | name + description（进 system，~100 tokens/ skill） | harness 扫描 `.agents/skills/` |
| 加载方式 | 模型读 path 下全文；hosted `skill_reference` 或 local path | 触发后 bash `cat SKILL.md`；资源/脚本再按需 | 挂载进 sandbox 后自动注册 |
| 托管附着 | Responses shell `environment.skills`；Agents API 用 `capability_directories` | API `container` + code execution；Managed Agents `skills` 字段；Claude Code 文件系统 | `environment.sources` inline/Git/GCS；或 managed agent `base_environment` |
| 版本/上传 | Skills API 版本化 zip；curated 如 `openai-spreadsheets` | Skills API / claude.ai 上传；表面不互通 | 无独立 Skills 产品 API（随 agent/环境文件走） |
| 安全强调 | 勿对终端用户开放任意 Skills 目录；等同特权指令 | 仅信可信源；企业可扫内容 | 与沙箱网络 allowlist / hooks 联动 |

## 实践建议

1. **可移植内容**：按 agentskills.io 写 `SKILL.md`，再分别接到各家挂载点。
2. **触发质量**：description 写清「做什么 + 何时用」。
3. **权限**：Skills 可驱动 shell/脚本，按最高权限审查；网络场景叠加各家沙箱策略。

## 建议精读原文

- https://agentskills.io/specification
- 各厂商 Skills / custom-agents 页面（上表链接）
