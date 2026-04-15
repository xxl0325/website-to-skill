# Contributing

## 添加新的模板

1. 在 `templates/` 目录创建新的 `.j2` 模板
2. 在 `generator/` 中添加对应的生成逻辑
3. 运行测试验证

## 添加新的提取器

1. 在 `scraper/` 目录添加新的提取模块
2. 更新 `analyzer.py` 中的 `analyze_design()` 函数
3. 添加对应的模板渲染逻辑

## 测试

```bash
# 运行测试
python -m pytest tests/

# 测试单个网站
python generate_skill.py https://example.com --name example
```
