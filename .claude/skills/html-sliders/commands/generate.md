# /html-generate 命令详解

## 前置条件

执行此命令前需要：
1. 已完成 `/html-analyze` 生成分段结构
2. 已完成 `/html-design` 确定设计规范

## 执行流程

### 1. 收集信息
- 分段结构（来自 analyze）
- 设计规范（来自 design）
- 原始文稿内容

### 2. 生成 HTML

#### 基础结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>${styles}</style>
</head>
<body>
  ${navigation}
  ${sections}
  <script>${scripts}</script>
</body>
</html>
```

#### 分段生成逻辑

**Hero 区**：
```html
<section class="hero" id="hero">
  <div class="hero-bg"></div>
  <div class="particles" id="particles"></div>
  <div class="hero-content">
    <div class="hero-badge">${badge}</div>
    <h1>${title}</h1>
    <p>${subtitle}</p>
    ${stats}
  </div>
</section>
```

**Stats 区**：
```html
<div class="stats">
  ${items.map(item => `
    <div class="stat">
      <div class="stat-v">${item.value}</div>
      <div class="stat-l">${item.label}</div>
    </div>
  `).join('')}
</div>
```

**Cards 区**：
```html
<section class="s" id="${id}">
  <div class="s-head rv">
    <div class="s-num">${partNumber}</div>
    <h2 class="s-title">${title}</h2>
    <p class="s-sub">${subtitle}</p>
  </div>
  <div class="grid grid-2">
    ${cards.map(card => `
      <div class="card rv">
        <div class="card-title">${card.title}</div>
        <div class="card-text">${card.content}</div>
      </div>
    `).join('')}
  </div>
</section>
```

**Quote 区**：
```html
<div class="quote rv">
  ${content}
  <span class="author">${author}</span>
</div>
```

**Code 区**：
```html
<div class="code rv">
  ${highlightedCode}
</div>
```

**Ending 区**：
```html
<section class="s ending" id="end">
  <div class="s-head rv">
    <h2 class="s-title">${title}</h2>
  </div>
  <div class="quote rv">${summary}</div>
  ${callToAction}
</section>
```

### 3. 注入 CSS

CSS 按以下顺序注入：
1. **Reset** - 基础重置
2. **Variables** - CSS 变量（来自设计规范）
3. **Base** - 基础样式（字体、滚动条）
4. **Navigation** - 导航栏样式
5. **Sections** - 分段样式
6. **Components** - 组件样式（card、quote、code等）
7. **Animations** - 动画定义

### 4. 注入 JavaScript

JavaScript 功能：
1. **粒子动画** - 生成浮动粒子
2. **滚动揭示** - IntersectionObserver
3. **弹幕系统** - 滚动弹幕
4. **平滑滚动** - 锚点跳转

```javascript
// 粒子动画
const particles = document.getElementById('particles');
const colors = ['#00d4ff', '#b44aff', '#ff4a8d', '#00ff88'];
for (let i = 0; i < 30; i++) {
  const p = document.createElement('div');
  p.className = 'particle';
  p.style.left = Math.random() * 100 + '%';
  p.style.background = colors[Math.floor(Math.random() * colors.length)];
  p.style.animationDuration = (8 + Math.random() * 12) + 's';
  particles.appendChild(p);
}

// 滚动揭示
const observer = new IntersectionObserver(entries => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('vis'), i * 60);
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.rv').forEach(el => observer.observe(el));
```

### 5. 写入文件

- 默认文件名：`output.html`
- 写入位置：当前工作目录
- 使用 Write 工具写入

## 输出示例

```
✅ HTML 文件生成完成！

📄 文件信息：
- 文件名：output.html
- 大小：约 45KB
- 分段数：7
- 风格：科技暗黑

🎯 使用方法：
1. 双击 output.html 在浏览器中打开
2. 或拖拽到浏览器窗口中
3. 支持移动端响应式浏览

✨ 包含特效：
- 粒子动画（30个浮动粒子）
- 滚动揭示动画
- 平滑滚动导航
- 可选弹幕特效
```

## 质量检查

生成后自动检查：
- [ ] HTML 语法正确
- [ ] CSS 变量完整
- [ ] JavaScript 无语法错误
- [ ] 所有分段 ID 唯一
- [ ] 导航链接有效
- [ ] 响应式样式完整
