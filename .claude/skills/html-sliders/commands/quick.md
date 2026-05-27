# /html-quick 命令详解

## 执行流程

### 1. 读取并分析文稿
- 读取用户指定的 Markdown 文件
- 识别文稿结构：标题层级、段落、列表、代码块、引用等
- 提取关键信息：数字统计、重点语句、代码片段

### 2. 智能分段
根据内容自动分配分段类型：

| 内容特征 | 分段类型 |
|---------|---------|
| 文档标题 + 简介 | `hero` |
| 多个数字/指标 | `stats` |
| 多个并列要点 | `cards` |
| 引用/名言 | `quote` |
| 代码片段 | `code` |
| 步骤/流程 | `flow` |
| 重点提示 | `highlight` |
| 对比内容 | `two-col` |
| 总结/号召 | `ending` |

### 3. 应用风格
根据 `--style` 参数选择预设风格配置，包括：
- CSS 变量（颜色、背景、渐变）
- 字体设置
- 卡片样式
- 动画效果

### 4. 生成 HTML
- 组装 HTML 结构
- 注入 CSS 样式
- 添加 JavaScript 交互
- 写入输出文件

## 生成规范

### HTML 结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[文档标题]</title>
  <style>
    /* 内联 CSS */
  </style>
</head>
<body>
  <!-- 导航 -->
  <nav class="nav">...</nav>

  <!-- 各分段 -->
  <section class="s" id="section-1">...</section>
  <section class="s" id="section-2">...</section>
  ...

  <!-- JavaScript -->
  <script>...</script>
</body>
</html>
```

### CSS 规范
- 使用 CSS 变量管理配色
- 响应式设计（mobile-first）
- 动画使用 `transition` 和 `@keyframes`
- 支持 `prefers-reduced-motion`

### JavaScript 规范
- 使用 IntersectionObserver 实现滚动揭示
- 粒子动画使用纯 DOM 操作
- 弹幕使用 CSS animation

## 示例输出

输入 Markdown：
```markdown
# Claude Code 源码分析

## 核心数据
- 1902 个源码文件
- 47.7 万行代码
- 6 个内置 Agent

## 核心能力
1. 提示词动态拼装
2. Agent 分工调度
3. 工具安全管线
```

输出 HTML 结构：
- Hero 区：标题 + 简介
- Stats 区：3 个数据卡片
- Cards 区：3 个能力卡片
- Ending 区：总结

## 错误处理

| 错误 | 处理方式 |
|------|---------|
| 文件不存在 | 提示用户并提供正确路径 |
| 文件为空 | 生成最小化模板 HTML |
| 格式无法识别 | 将内容作为纯文本处理 |
