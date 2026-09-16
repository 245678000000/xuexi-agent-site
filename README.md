# Agent 学习站

将 Obsidian 库（`学习agent/`）生成为可读的中文静态站点，便于部署到 Vercel。

## 本地构建

```bash
# 依赖（Python 3.10+）
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 生成站点
python3 build.py
# 或
./build.sh
# 或
npm run build
```

输出目录：`dist/`（打开 `dist/index.html` 预览）。

## 从 Mac 上的 Obsidian 库同步

1. 在 Mac 上打开 vault，确认内容在 `学习agent/`（或等价根目录）。
2. 把该文件夹拷到本仓库可访问的路径（或解压 tarball）。
3. 运行：

```bash
./scripts/sync-from-vault.sh /path/to/学习agent
# 若路径是含有 学习agent/ 子目录的解压根，也可直接传该根路径
```

脚本会：**清空并替换** `content/` → 重新 `build` → 产物在 `dist/`。

4. 提交并推送：

```bash
git add content dist
git commit -m "sync vault content"
git push
```

Vercel 若已连接本仓库，推送后会自动按下方设置重新构建。

## 仓库结构

| 路径 | 说明 |
|------|------|
| `content/` | 从 vault 同步的 Markdown（勿手写课程正文） |
| `build.py` | Markdown → HTML（含 wikilink 尽力解析） |
| `static/style.css` | 主题 |
| `dist/` | 构建输出 |
| `scripts/sync-from-vault.sh` | 同步入口 |
| `requirements.txt` | `markdown==3.7` |
| `vercel.json` | Vercel 构建设置 |

## Vercel 建议设置

若使用本仓库的 `vercel.json`，一般无需在面板再改。手动配置时：

| 项 | 值 |
|----|-----|
| Framework Preset | Other |
| Build Command | `pip install -r requirements.txt && python3 build.py` |
| Output Directory | `dist` |
| Install Command | （可留空；构建命令已含 pip） |
| Node.js Version | 18+（仅用于触发构建脚本，逻辑在 Python） |

也可用 `npm run build`（见 `package.json`），但需保证构建镜像里有 `python3` 与 pip。

## Wikilink 说明

支持尽力改写：

- `[[笔记名]]` / `[[路径/笔记]]`
- `[[路径/笔记\|别名]]`
- 指向目录的链接（如 `[[日记]]`）→ 目录索引页

限制：

- 不解析 embed（`![[...]]`）为嵌入内容，仅当普通链接处理（若写成 `![[` 需在源中避免或后续增强）。
- 块引用 `[[Note^block]]`、复杂 heading 锚点仅为尽力匹配。
- 重名笔记按「与当前文件路径更近」消歧；仍可能点错时请改用全路径 wikilink。
- Mermaid 以源码块展示，不在浏览器端渲染。
- 任务列表复选框为只读展示（网页不写回 vault）。

## 许可

笔记内容归属原作者；本生成器脚本可按需修改。
