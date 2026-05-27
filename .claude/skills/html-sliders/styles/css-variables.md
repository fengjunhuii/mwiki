# CSS 变量定义

基于 `html_sider.html` 提取的核心 CSS 变量系统。

## 基础变量

```css
:root {
  /* 背景色 */
  --bg: #0a0a0f;      /* 主背景 */
  --bg2: #12121a;     /* 次级背景 */
  --card: #1a1a2e;    /* 卡片背景 */
  --card2: #222240;   /* 次级卡片 */

  /* 主题色 */
  --blue: #00d4ff;    /* 蓝色 */
  --purple: #b44aff;  /* 紫色 */
  --pink: #ff4a8d;    /* 粉色 */
  --green: #00ff88;   /* 绿色 */
  --orange: #ff8c00;  /* 橙色 */
  --yellow: #ffd700;  /* 黄色 */
  --red: #ff4444;     /* 红色 */

  /* 文字色 */
  --text: #e8e8f0;    /* 主文字 */
  --text2: #a0a0b8;   /* 次级文字 */
  --muted: #666680;   /* 弱化文字 */

  /* 渐变 */
  --gm: linear-gradient(135deg, #00d4ff, #b44aff, #ff4a8d);  /* 主渐变 */
  --gf: linear-gradient(135deg, #ff4444, #ff8c00, #ffd700);  /* 火焰渐变 */
}
```

## 语义变量

```css
:root {
  /* 状态色 */
  --success: var(--green);
  --warning: var(--orange);
  --error: var(--red);
  --info: var(--blue);

  /* 边框 */
  --border: rgba(180, 74, 255, 0.12);
  --border-hover: rgba(0, 212, 255, 0.3);

  /* 阴影 */
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  --shadow-hover: 0 15px 40px rgba(0, 0, 0, 0.4);
}
```

## 组件变量

```css
:root {
  /* 导航栏 */
  --nav-bg: rgba(10, 10, 15, 0.88);
  --nav-border: rgba(180, 74, 255, 0.15);
  --nav-height: 56px;

  /* 卡片 */
  --card-radius: 16px;
  --card-padding: 1.8rem;
  --card-border: rgba(180, 74, 255, 0.12);

  /* 按钮 */
  --btn-radius: 25px;
  --btn-padding: 0.8rem 2.5rem;

  /* 代码块 */
  --code-bg: #0d1117;
  --code-border: rgba(180, 74, 255, 0.12);
  --code-radius: 10px;

  /* 引用 */
  --quote-border: var(--purple);
  --quote-bg: rgba(180, 74, 255, 0.04);
}
```

## 动画变量

```css
:root {
  /* 过渡 */
  --transition-fast: 0.2s;
  --transition-normal: 0.3s;
  --transition-slow: 0.5s;

  /* 动画 */
  --reveal-duration: 0.6s;
  --reveal-distance: 25px;
}
```

## 标签颜色

```css
/* 标签类 */
.tag-b {
  background: rgba(0, 212, 255, 0.1);
  color: var(--blue);
  border: 1px solid rgba(0, 212, 255, 0.2);
}

.tag-p {
  background: rgba(180, 74, 255, 0.1);
  color: var(--purple);
  border: 1px solid rgba(180, 74, 255, 0.2);
}

.tag-g {
  background: rgba(0, 255, 136, 0.1);
  color: var(--green);
  border: 1px solid rgba(0, 255, 136, 0.2);
}

.tag-o {
  background: rgba(255, 140, 0, 0.1);
  color: var(--orange);
  border: 1px solid rgba(255, 140, 0, 0.2);
}

.tag-r {
  background: rgba(255, 68, 68, 0.1);
  color: var(--red);
  border: 1px solid rgba(255, 68, 68, 0.2);
}
```

## 响应式断点

```css
/* 移动端 */
@media (max-width: 768px) {
  :root {
    --card-padding: 1.2rem;
    --nav-height: 50px;
  }
}

/* 平板 */
@media (min-width: 769px) and (max-width: 1024px) {
  :root {
    --card-padding: 1.5rem;
  }
}
```
