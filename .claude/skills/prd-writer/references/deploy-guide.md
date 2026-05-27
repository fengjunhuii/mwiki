# Cloudflare Pages 部署指南

## 前置准备

### 1. 创建 API Token

访问 https://dash.cloudflare.com/profile/api-tokens → **Create Token** → **Custom Token**

| 权限 | 资源范围 | 是否必须 |
|------|---------|---------|
| `Cloudflare Pages:Edit` | Account | ✅ 必须 |
| `Account Settings:Read` | Account | ✅ 必须 |
| `Zone:Read` | All Zones | 自定义域名时需要 |
| `DNS:Edit` | 指定 Zone | 绑定域名时需要 |

### 2. 获取 Account ID

在 Cloudflare Dashboard 右侧边栏复制 **Account ID**。

### 3. 配置环境变量

```bash
export CLOUDFLARE_API_TOKEN="your-api-token"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"
```

---

## 部署方式

### 方式 1：Wrangler CLI（推荐）

```bash
# 安装
npm install -g wrangler

# 交互式登录（浏览器授权）
wrangler login

# 部署
cd prototype
wrangler pages deploy . --project-name=your-project-name
```

### 方式 2：Dashboard 手动上传

1. 访问 https://dash.cloudflare.com
2. 进入 **Workers & Pages** → **Create**
3. 选择 **Pages** → **Upload assets**
4. 拖入 `prototype` 文件夹
5. 设置项目名称，点击部署

### 方式 3：连接 Git 仓库

1. 进入 **Workers & Pages** → **Create** → **Connect to Git**
2. 选择 GitHub 仓库
3. 构建设置：
   - **Build command**: 留空（静态站点）
   - **Build output directory**: `/` 或 `public`
4. 点击 **Save and Deploy**

---

## 自定义域名（可选）

1. 进入项目设置 → **Custom domains**
2. 点击 **Set up a custom domain**
3. 输入域名，按提示配置 DNS

---

## 优势

- ✅ **国内可访问** - 无需科学上网
- ✅ **免费额度充足** - 每月 500 次构建
- ✅ **自动 HTTPS** - 免费 SSL 证书
- ✅ **全球 CDN** - 访问速度快
- ✅ **无需备案** - pages.dev 域名

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| 404 错误 | 确保 `index.html` 在根目录 |
| 路由问题 | 添加 `_redirects` 文件：`/* /index.html 200` |
| 缓存问题 | Cloudflare 自动处理，无需额外配置 |

## 示例地址

部署后获得：
```
https://your-project.pages.dev
```
