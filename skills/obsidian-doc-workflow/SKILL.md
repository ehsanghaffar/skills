---
name: obsidian-doc-workflow
description: Create, update, classify, and archive Obsidian documentation documents following structured vault conventions and templates.
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - obsidian-cli
        - python3
      env:
        - OBSIDIAN_VAULT_PATH
    emoji: "📚"
    homepage: "https://clawhub.ai/agent/obsidian-doc-workflow"
    models:
      - gpt-4
      - deepseek-v4-flash
      - claude-sonnet-4
      - m3o-mini
      - gemini-2.0-flash
---

# Obsidian Documentation Workflow

This skill manages structured documentation in an Obsidian vault following a formal documentation system with strict conventions.

## Vault Path

Resolved vault path is typically(Mac):
${OBSIDIAN_VAULT_PATH:-/Users/${USER}/.obsidian}

The vault uses three main sections:
- `01 Projects/` - Project-specific documentation
- `02 Shared Knowledge/` - Reusable engineering patterns
- `00 Meta/` - Vault standards, templates, and guidance

## Document Creation

### For Project Documents

Use the project root template. Always start with `Project Overview.md` in the project root, then architecture, guides, API reference, and so on.

**Example project structure:**
```
01 Projects/{Project}/
├── Project Overview.md
├── Architecture & Tech Stack.md
├── Development Guide.md
├── Component & API Reference.md
├── Testing Guide.md
├── Deployment & Infrastructure.md
├── Maintenance Board.md
├── Changelog.md
└── <Architecture>, <Services>, <Database>, <Guides>, etc.
```

**Standard frontmatter:**
```yaml
---
type: project|architecture|guide|reference|research|runbook|maintenace|changelog
project: "Project Name"
status: active|archived|deprecated
area: frontend|backend|infra|security|testing|devops
created: 2026-09-19
updated: 2026-09-19
tags: [project-slug, area, type]
related_projects: []
---
```

### For Shared Knowledge Documents

Use the `Concept.md` or `Tool.md` templates.

**Standard frontmatter:**
```yaml
---
type: concept|tool|architecture|guide
status: active|archived
area: patterns|frontend|backend|testing|devops
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [category, subcategory, type]
related_projects: [Project A, Project B]
---
```

## Classification Rules

### Project vs Shared Knowledge

- **Project knowledge** → `01 Projects/{Project}/` (obsoletes when project disappears)
- **Reusable patterns** → `02 Shared Knowledge/` (remains useful after projects are gone)

### Residence Categories

- Project-specific implementations → Project folder
- General patterns, tech guides, security practices, deployment strategies → Shared Knowledge
- External references → `03 Resources/`

**Examples:**
- `Backend Integration Guide` (specific to a project) → Project folder
- `Monorepo Patterns` (any team can use) → Shared Knowledge
- `Vercel deployment docs` → Resources

## Templates

Respective templates in `00 Meta/Templates/`:
- `Project Overview.md`
- `Architecture.md`
- `Development Guide.md`
- `Technical Guide.md`
- `API Reference.md`
- `Testing Guide.md`
- `Deployment & Infrastructure.md`
- `ADR.md`
- `Decision.md`
- `Research.md`
- `Concept.md`
- `Tool.md`
- `Runbook.md`
- `Maintenance Item.md`
- `Resource.md`

## Linking Rules

- Use Wikilinks `[[Document Name]]` for internal links
- Cross-folder links: `[[Folder/Document Name]]`
- Deep links: `[[Document Name#Section Heading]]`
- Never create giant navigation pages — use links to build a knowledge graph

## Tagging Convention

Tags are lowercase, kebab-case, max 5 tags per document.

**Categories:**
- Technology: `nextjs`, `typescript`, `prisma`, `turborepo`, `ltit-tool`
- Domain: `architecture`, `security`, `testing`, `deployment`, `frontend`, `backend`
- Type: `adr`, `guide`, `reference`, `research`, `runbook`, `concept`, `tool`
- Status: `active`, `archived`, `deprecated`, `draft`
- Project: `project-one`, `project-two`, `project-three`

## Creating New Documents

Follow this sequence:
1. Determine document type and location (Project vs Shared Knowledge)
2. Use the appropriate template from `00 Meta/Templates/`
3. Fill all required frontmatter with current date
4. Write content following structure defined by the template
5. Link to related documents (bidirectional where appropriate)
6. Place in the correct folder

## Validating Created Documents

Before considering a document complete:

- [ ] Frontmatter complete and accurate (all required fields present)
- [ ] Title matches filename (without extension)
- [ ] Structure follows document template
- [ ] All internal wikilinks resolve
- [ ] External links have descriptive text
- [ ] No broken wikilinks
- [ ] Has 1 domain tag and 1 document type tag
- [ ] Code blocks specify language
- [ ] Updated date reflects current date
- [ ] No generic Chinese messages or placeholders

## Archive Process

When content is obsolete or superseded:

1. Move file: `04 Archives/Deprecated/`, `Superseded/`, or `Historical/` as appropriate
2. Change `status` to `archived` or `deprecated`
3. Add link from new/superseding document

**Archive destinations:**
- Deprecated → Obsolete technology, outdated patterns, deprecated tools
- Superseded → Replaced by newer version or consolidated docs
- Historical → Completed reviews, old decisions, old snapshots

## Special Guardrails

- Never delete content without archiving first
- Never rewrite technical content for flavor/style only
- Never create empty documents just to satisfy structure
- Always keep `00 Meta/Templates/` as canonical source for document structures
- All documents use English primarily; Persian content is translated/summarized in English
- Frontmatter property order: `type` → `status` → `project` (project-scoped) → `area` → `created` → `updated` → `tags` → additional fields

---

# Obsidian 文档工作流

此技能按照严格的文档规范和模板管理 Obsidian 仓库的结构化文档。

## 仓库路径

解析后的仓库路径通常为：
${OBSIDIAN_VAULT_PATH:-/Users/${USER}/.obsidian}

仓库使用三个主要部分：
- `01 Projects/` - 项目专用文档
- `02 Shared Knowledge/` - 可复用的工程模式
- `00 Meta/` - 仓库标准、模板和指导

## 文档创建

### 项目文档

使用项目根模板。始终从项目根目录的 `Project Overview.md` 开始，然后是架构、指南、API 参考，依此类推。

**示例项目结构：**
```
01 Projects/{Project}/
├── Project Overview.md
├── Architecture & Tech Stack.md
├── Development Guide.md
├── Component & API Reference.md
├── Testing Guide.md
├── Deployment & Infrastructure.md
├── Maintenance Board.md
├── Changelog.md
└── <Architecture>, <Services>, <Database>, <Guides>, 等。
```

**标准 frontmatter：**
```yaml
---
type: project|architecture|guide|reference|research|runbook|maintenance|changelog
project: "项目名称"
status: active|archived|deprecated
area: frontend|backend|infra|security|testing|devops
created: 2026-09-19
updated: 2026-09-19
tags: [project-slug, area, type]
related_projects: []
---
```

### 共享知识文档

使用 `Concept.md` 或 `Tool.md` 模板。

**标准 frontmatter：**
```yaml
---
type: concept|tool|architecture|guide
status: active|archived
area: patterns|frontend|backend|testing|devops
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [category, subcategory, type]
related_projects: [项目 A, 项目 B]
---
```

## 分类规则

### 项目 vs 共享知识

- **项目知识** → `01 Projects/{Project}/`（项目消失时变为过期）
- **可复用模式** → `02 Shared Knowledge/`（项目消失后仍然有用）

### 归属分类

- 项目专用实现 → 项目文件夹
- 一般模式、技术指南、安全实践、部署策略 → 共享知识
- 外部参考 → `03 Resources/`

**示例：**
- `Backend Integration Guide`（专用于某个项目）→ 项目文件夹
- `Monorepo 模式`（任何团队均可使用）→ 共享知识
- `Vercel 部署文档` → Resources

## 模板

各模板位于 `00 Meta/Templates/`：
- `Project Overview.md`
- `Architecture.md`
- `Development Guide.md`
- `Technical Guide.md`
- `API Reference.md`
- `Testing Guide.md`
- `Deployment & Infrastructure.md`
- `ADR.md`
- `Decision.md`
- `Research.md`
- `Concept.md`
- `Tool.md`
- `Runbook.md`
- `Maintenance Item.md`
- `Resource.md`

## 链接规则

- 使用 Wikilinks `[[文档名称]]` 进行内部链接
- 跨文件夹链接：`[[文件夹/文档名称]]`
- 深度链接：`[[文档名称#章节标题]]`
- 不要创建大型导航页 — 通过链接构建知识图谱

## 标签约定

标签为小写，kebab-case，每个文档最多5个标签。

**类别：**
- 技术：`nextjs`、`typescript`、`prisma`、`turborepo`、`lti`
- 领域：`architecture`、`security`、`testing`、`deployment`、`frontend`、`backend`
- 类型：`adr`、`guide`、`reference`、`research`、`runbook`、`concept`、`tool`
- 状态：`active`、`archived`、`deprecated`、`draft`
- 项目：`project-one`、`project-two`、`talkway.ir`

## 创建新文档

按此顺序操作：
1. 确定文档类型和位置（项目 vs 共享知识）
2. 使用 `00 Meta/Templates/` 中相应的模板
3. 用当前日期填写所有必需的 frontmatter
4. 按模板定义的结构编写内容
5. 链接到相关文档（适当时双向链接）
6. 放入正确的文件夹

## 验证创建的文档

在考虑文档完成之前：

- [ ] Frontmatter 完整准确（所有必需字段存在）
- [ ] 标题与文件名匹配（不带扩展名）
- [ ] 结构遵循文档模板
- [ ] 所有内部 wikilinks 可解析
- [ ] 外部链接有描述性文本
- [ ] 无损坏的 wikilinks
- [ ] 有 1 个领域标签和 1 个文档类型标签
- [ ] 代码块指定语言
- [ ] 更新日期反映当前日期
- [ ] 无通用中文消息或占位符

## 归档流程

当内容过期或被取代时：

1. 将文件移动到 `04 Archives/Deprecated/`、`Superseded/` 或 `Historical/`（视情况而定）
2. 将 `status` 更改为 `archived` 或 `deprecated`
3. 在新/取代文档中添加链接

**归档目的地：**
- Deprecated → 过时的技术、过时的模式、已弃用的工具
- Superseded → 被新版本或合并文档取代
- Historical → 已完成的审查、旧决策、过时的快照

## 特殊防护规则

- 除非归档，否则永远不要删除内容
- 不要仅为了风格重写技术内容
- 不要由于满足结构而创建空文档
- 始终将 `00 Meta/Templates/` 视为文档结构的权威来源
- 所有文档主要使用英文；波斯语内容翻译/总结为英文
- Frontmatter 属性顺序：`type` → `status` → `project`（项目范围）→ `area` → `created` → `updated` → `tags` → 额外字段