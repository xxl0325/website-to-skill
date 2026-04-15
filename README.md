# Website to DESIGN.md

根据网站 URL 或本地 HTML 文件生成详细的设计系统文档（DESIGN.md）。

生成的 DESIGN.md 包含 9 个完整章节，可以作为 prompt 交给大模型来还原网站 UI。

## 功能

- 抓取网站 HTML 和 CSS（支持本地文件或 URL）
- 使用 LLM 分析设计元素
- 生成标准 DESIGN.md 格式（9 个章节）：
  1. Visual Theme & Atmosphere
  2. Color Palette & Roles
  3. Typography Rules
  4. Component Stylings
  5. Layout Principles
  6. Depth & Elevation
  7. Do's and Don'ts
  8. Responsive Behavior
  9. Agent Prompt Guide

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器（如需抓取 URL）
playwright install
```

## 使用

### 从本地 HTML 文件生成

```bash
python generate_skill.py ./path/to/website.html --name tesla --output ./output
```

### 从 URL 生成

```bash
python generate_skill.py https://example.com --name example --output ./output
```

### 参数

| 参数 | 说明 |
|------|------|
| `input` | 本地 HTML 文件路径或网站 URL |
| `--name` | 设计系统名称（必需） |
| `--output` | 输出目录（默认：./output） |
| `--css` | 单独的 CSS 文件路径（可选） |
| `--model` | 使用的模型（默认：从环境变量读取） |

## 输出结构

```
output/tesla/
├── DESIGN.md         # 详细设计系统文档（9 个章节）
└── design_data.json  # 结构化数据（调试用）
```

## DESIGN.md 示例结构


生成的文档包含：

- **视觉主题**：2-3 段设计理念、情感基调、摄影/插图风格
- **颜色系统**：每个颜色有命名、Hex、RGB、使用场景描述
- **排版规则**：字体家族、层级表格、排版原则
- **组件样式**：Buttons、Cards、Navigation、Inputs 等详细 CSS 值
- **布局原则**：间距系统、网格、留白哲学
- **深度层级**：阴影使用哲学、装饰性深度
- **Do's and Don'ts**：8-10 条具体规则
- **响应式行为**：断点表格、触摸目标、折叠策略
- **Agent Prompt 指南**：快速颜色参考、示例 Prompt、迭代建议

## 环境变量

```bash
export ANTHROPIC_AUTH_TOKEN="your-api-key"
export ANTHROPIC_BASE_URL="https://api.anthropic.com"  # 或使用代理
export ANTHROPIC_MODEL="claude-sonnet-4-0"
```

## 示例

```bash
# 从本地 HTML 生成 Tesla 设计文档
python generate_skill.py ./tesla-demo.html --name tesla --output ./test-output

# 从 URL 生成（需要网络访问）
python generate_skill.py https://www.tesla.com --name tesla --output ./output

# 指定模型
python generate_skill.py ./site.html --name mysite --model claude-opus-4-0
```

## 常见问题

**Q: 生成的内容不够详细？**

A: 确保输入的 HTML/CSS 包含足够的样式信息。如果只提供了简单的 demo HTML，LLM 可能无法推断完整的设计系统。

**Q: 抓取失败？**

A: 检查网络连接，或尝试使用本地 HTML 文件。

**Q: 如何使用生成的 DESIGN.md？**

A: 将 DESIGN.md 文件内容复制给大模型，它可以用来还原网站 UI 或生成类似的组件代码。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
