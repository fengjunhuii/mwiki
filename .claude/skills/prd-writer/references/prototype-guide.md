# 原型生成指南

## 技术规格

生成单文件 HTML 原型，可直接在浏览器打开：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[产品名称] - 原型</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 自定义样式 */
    </style>
</head>
<body>
    <!-- 页面内容 -->
    <script>
        // 交互逻辑
    </script>
</body>
</html>
```

---

## 设计风格选项

### 1. Glassmorphism（毛玻璃）
```html
<div class="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500">
  <div class="backdrop-blur-lg bg-white/30 border border-white/20 rounded-xl p-6 shadow-lg">
    <!-- 毛玻璃卡片 -->
  </div>
</div>
```

### 2. Minimalism（极简）
```html
<div class="bg-white max-w-2xl mx-auto py-12 px-6">
  <h1 class="text-4xl font-light text-gray-900 mb-4">标题</h1>
  <p class="text-gray-500 leading-relaxed">内容</p>
</div>
```

### 3. Material Design
```html
<div class="bg-white shadow-md rounded-lg p-4 hover:shadow-lg transition-shadow">
  <div class="text-sm text-gray-500 uppercase tracking-wide">标签</div>
  <div class="text-xl font-medium mt-1">标题</div>
</div>
```

### 4. Dark Mode（深色模式）
```html
<div class="dark">
  <div class="bg-gray-900 text-white min-h-screen">
    <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <!-- 深色卡片 -->
    </div>
  </div>
</div>
```

### 5. 暗色/亮色模式切换
```javascript
function initTheme() {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.classList.toggle('dark', saved === 'dark');
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// Tailwind config 需开启 darkMode: 'class'
// <script>tailwind.config = { darkMode: 'class' }</script>
```

---

## 必备交互组件

### 1. 导航栏
```html
<nav class="fixed top-0 w-full bg-white shadow-sm z-50">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <div class="font-bold text-xl">Logo</div>
        <div class="flex gap-4">
            <a href="#" class="hover:text-blue-600">首页</a>
            <a href="#" class="hover:text-blue-600">功能</a>
        </div>
    </div>
</nav>
```

### 2. 表单校验
```javascript
function validateForm() {
    const input = document.getElementById('phone');
    const error = document.getElementById('error');
    if (!/^1[3-9]\d{9}$/.test(input.value)) {
        error.textContent = '请输入正确的手机号';
        error.classList.remove('hidden');
        return false;
    }
    error.classList.add('hidden');
    return true;
}
```

### 3. Loading 状态
```javascript
function submitWithLoading(btn) {
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.innerHTML = '<svg class="animate-spin h-5 w-5 mr-2 inline" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" opacity="0.25"></circle><path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>提交中...';

    setTimeout(() => {
        btn.disabled = false;
        btn.textContent = originalText;
    }, 2000);
}
```

### 4. Toast 提示
```javascript
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 px-6 py-3 rounded-lg text-white ${type === 'success' ? 'bg-green-500' : 'bg-red-500'} transition-opacity duration-300`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
```

### 5. 模态框/抽屉
```html
<div id="modal" class="fixed inset-0 bg-black/50 hidden items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-96">
        <h3 class="text-lg font-bold mb-4">标题</h3>
        <p>内容</p>
        <button onclick="closeModal()" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded">关闭</button>
    </div>
</div>
```

### 6. Tab 页面切换
```javascript
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('border-blue-600', 'text-blue-600'));
    document.getElementById(tabId).classList.remove('hidden');
    event.target.classList.add('border-blue-600', 'text-blue-600');
}
```

### 7. 空状态引导
```html
<div class="flex flex-col items-center justify-center py-16 text-center">
    <svg class="w-16 h-16 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
    </svg>
    <p class="text-gray-500 mb-2">暂无数据</p>
    <button class="text-blue-600 hover:text-blue-700 text-sm" onclick="showCreate()">+ 新建第一条</button>
</div>
```

### 8. 分页组件
```html
<div class="flex items-center justify-between py-3">
    <span class="text-sm text-gray-500">共 48 条，第 2/5 页</span>
    <div class="flex gap-1">
        <button onclick="changePage(-1)" class="px-3 py-1 rounded border text-sm hover:bg-gray-50 disabled:opacity-40">上一页</button>
        <button class="px-3 py-1 rounded bg-blue-600 text-white text-sm">2</button>
        <button onclick="changePage(1)" class="px-3 py-1 rounded border text-sm hover:bg-gray-50">下一页</button>
    </div>
</div>
```

### 9. 下拉菜单
```html
<div class="relative inline-block">
    <button onclick="toggleDropdown()" class="px-4 py-2 border rounded-lg hover:bg-gray-50">
        操作 ▾
    </button>
    <div id="dropdown" class="absolute right-0 mt-2 w-40 bg-white border rounded-lg shadow-lg hidden z-10">
        <a href="#" class="block px-4 py-2 hover:bg-gray-50 text-sm">编辑</a>
        <a href="#" class="block px-4 py-2 hover:bg-gray-50 text-sm text-red-600">删除</a>
    </div>
</div>
<script>
function toggleDropdown() {
    document.getElementById('dropdown').classList.toggle('hidden');
}
document.addEventListener('click', e => {
    if (!e.target.closest('.relative')) {
        document.querySelectorAll('#dropdown').forEach(el => el.classList.add('hidden'));
    }
});
</script>
```

---

## 响应式适配

```html
<!-- 移动端汉堡菜单 -->
<button class="md:hidden" onclick="toggleMenu()">
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
    </svg>
</button>

<!-- 响应式网格 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- 卡片 -->
</div>
```

---

## 模拟数据

```javascript
const mockData = {
    users: [
        { id: 1, name: '张三', phone: '13800138001', status: '正常' },
        { id: 2, name: '李四', phone: '13800138002', status: '禁用' },
    ],
    orders: [
        { id: 'ORD001', amount: 299, status: '待支付', time: '2024-01-15 10:30' },
        { id: 'ORD002', amount: 599, status: '已完成', time: '2024-01-14 15:20' },
    ]
};
```

---

## UI 质量检查

交付原型前验证：

### 视觉质量
- [ ] 不使用 emoji 作为图标（使用 SVG）
- [ ] 所有图标来自统一图标库（Heroicons/Lucide）
- [ ] Hover 状态不会导致布局偏移
- [ ] 使用语义化主题色（`bg-primary`）

### 交互
- [ ] 所有可点击元素有 `cursor-pointer`
- [ ] Hover 状态提供清晰视觉反馈
- [ ] 过渡动画平滑（150-300ms）
- [ ] 键盘导航时焦点状态可见

### 亮/暗模式
- [ ] 亮色模式文字有足够对比度（4.5:1 最低）
- [ ] 玻璃/透明元素在亮色模式下可见
- [ ] 边框在两种模式下都可见

### 无障碍
- [ ] 所有图片有 alt 文本
- [ ] 表单输入有 label
- [ ] 颜色不是唯一的指示器
- [ ] 尊重 `prefers-reduced-motion`
