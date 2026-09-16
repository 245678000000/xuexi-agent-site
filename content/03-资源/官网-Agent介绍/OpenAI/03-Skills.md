# OpenAI：Agent Skills

- **来源**：https://developers.openai.com/api/docs/guides/tools-skills
- **整理日期**：2026-09-16

## 官方要点

1. **Skill = 版本化目录 + `SKILL.md`（front matter + 指令）**，可附 scripts / references / assets；兼容开放标准 [Agent Skills](https://agentskills.io/home)。
2. **两种形态**：
   - **Hosted shell**：`tools[].environment.skills` 用 `skill_reference`（含 curated / 指定 version）
   - **Local shell**：不支持 `skill_reference`，改由本地 path 提供 skill 文件
3. **发现机制**：平台把 name / description / path 注入 user prompt；模型决定是否读取完整 `SKILL.md`。
4. **Agents API**：不把 skill 挂在 Responses 的 skill_reference 上，而是把 skill 目录放进 sandbox，并在 `environment.capability_directories` 注册父目录（最多 32 个绝对路径，目录须已存在）。
5. **上传与限制**：multipart 或 zip；单 skill 约 50MB zip / ≤500 文件 / 单文件 ≤25MB；需审查安全（等同特权指令+代码）。
6. **安全**：不要把开放 Skills 目录直接暴露给终端用户随意选择；敏感动作要审批；hosted 容器过期即丢文件。

## 对照学习点

| 本库概念 | 对应 |
| --- | --- |
| **目标** | description 决定何时触发 skill |
| **工具** | skill 常驱动 shell / scripts，本身偏「流程包」 |
| **循环** | 模型读 SKILL.md → 执行步骤 → 再观察结果 |
| **记忆** | 指令按需加载，不全量常驻上下文 |
| **沙箱** | hosted container 或 self-hosted capability dirs |

## 建议精读原文

- https://developers.openai.com/api/docs/guides/tools-skills.md
- https://agentskills.io/specification
- https://developers.openai.com/api/docs/guides/agents-api/configuration
