# Security Rules - MCLAUDE Project

> **版本**: v1.0
> **最后更新**: 2025-03-26
> **适用**: MCLAUDE 项目
> **优先级**: [MUST] 所有代码必须遵守

---

## 核心原则 [MUST]

### 永不信任用户输入
- **所有**用户输入都必须验证
- **所有**用户输入都必须清理
- 在**多个层次**验证输入（前端、后端、数据库）
- 使用**白名单**验证，而非黑名单

### 纵深防御
- 不要依赖单一安全措施
- 在多个层次实施安全控制
- 假设每个层次都可能失效
- 实施多层防御机制

### 最小权限原则
- 只授予必要的最小权限
- 使用角色-based 访问控制（RBAC）
- 定期审查和撤销不必要的权限
- 默认拒绝，明确允许

---

## Python 安全实践 [MUST]

### 输入验证
```python
# ❌ 错误：直接使用用户输入
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL 注入风险
    return db.execute(query)

# ✅ 正确：使用参数化查询
def get_user(user_id):
    # 验证 user_id 是数字
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID")

    query = "SELECT * FROM users WHERE id = ?"
    return db.execute(query, (user_id,))

# ✅ 正确：使用 ORM
def get_user(user_id):
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID")
    return User.query.filter_by(id=user_id).first()
```

### 密码处理
```python
import bcrypt
from getpass import getpass

# ✅ 正确：使用 bcrypt 哈希密码
def hash_password(password: str) -> str:
    # 生成盐值并哈希
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# ✅ 正确：验证密码
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )

# ❌ 错误：不要自己实现密码哈希
def bad_hash_password(password: str) -> str:
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()  # 不安全
```

### 敏感数据处理
```python
import logging

# ❌ 错误：记录敏感数据
logger.info(f"User logged in: {username}, password: {password}")

# ✅ 正确：不记录敏感数据
logger.info(f"User logged in: {username}")

# ✅ 正确：使用脱敏
def mask_sensitive_data(data: str, visible: int = 4) -> str:
    """脱敏敏感数据，只显示前几位"""
    if len(data) <= visible:
        return '*' * len(data)
    return data[:visible] + '*' * (len(data) - visible)

logger.info(f"API Key: {mask_sensitive_data(api_key)}")
```

### 文件上传安全
```python
import os
from werkzeug.utils import secure_filename

# ✅ 正确：安全的文件上传
def upload_file(file):
    # 1. 验证文件类型
    ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg'}
    filename = secure_filename(file.filename)

    if not any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise ValueError("Invalid file type")

    # 2. 验证文件大小
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise ValueError("File too large")

    # 3. 生成安全的文件名
    import uuid
    safe_filename = f"{uuid.uuid4()}_{filename}"

    # 4. 保存到非 web 可访问目录
    upload_path = os.path.join('/var/uploads', safe_filename)
    file.save(upload_path)

    return safe_filename
```

### 命令注入防护
```python
import subprocess

# ❌ 错误：直接使用用户输入执行命令
def process_file(filename):
    result = os.system(f"cat {filename}")  # 命令注入风险
    return result

# ✅ 正确：使用 subprocess 和参数列表
def process_file(filename):
    # 验证文件名
    if not filename.isalnum() and '/' not in filename:
        raise ValueError("Invalid filename")

    result = subprocess.run(
        ['cat', filename],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

# ✅ 正确：使用 shlex.quote（如果需要 shell=True）
import shlex
def process_file_shell(filename):
    safe_filename = shlex.quote(filename)
    result = subprocess.run(
        f'cat {safe_filename}',
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout
```

---

## C++ 安全实践 [MUST]

### 缓冲区溢出防护
```cpp
// ❌ 错误：不安全的字符串操作
char buffer[64];
strcpy(buffer, user_input);  // 缓冲区溢出风险

// ✅ 正确：使用安全的字符串操作
#include <string>
std::string str = user_input;

// ✅ 正确：使用带边界检查的函数
strncpy(buffer, user_input.c_str(), sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';

// ✅ 更好：使用 std::array
#include <array>
std::array<char, 64> buffer{};
std::strncpy(buffer.data(), user_input.c_str(), buffer.size() - 1);
```

### 智能指针和内存安全
```cpp
// ❌ 错误：裸指针，容易内存泄漏
void process() {
    User* user = new User();
    // 如果发生异常，内存泄漏
    delete user;
}

// ✅ 正确：使用智能指针
#include <memory>
void process() {
    std::unique_ptr<User> user(new User());
    // 自动释放内存，即使发生异常
}

// ✅ 更好：使用 make_unique（C++11 需要 C++14）
void process() {
    auto user = std::unique_ptr<User>(new User());
}
```

### 整数溢出防护
```cpp
#include <limits>
#include <stdexcept>

// ❌ 错误：可能整数溢出
int add(int a, int b) {
    return a + b;
}

// ✅ 正确：检查整数溢出
int safe_add(int a, int b) {
    if (b > 0 && a > std::numeric_limits<int>::max() - b) {
        throw std::overflow_error("Integer overflow");
    }
    if (b < 0 && a < std::numeric_limits<int>::min() - b) {
        throw std::overflow_error("Integer underflow");
    }
    return a + b;
}
```

---

## 数据库安全 [MUST]

### SQL 注入防护
```python
# ❌ 错误：字符串拼接 SQL
query = f"SELECT * FROM users WHERE name = '{username}'"
# username = "admin' OR '1'='1" 会导致 SQL 注入

# ✅ 正确：使用参数化查询
query = "SELECT * FROM users WHERE name = ?"
result = db.execute(query, (username,))

# ✅ 正确：使用 ORM
result = User.query.filter_by(name=username).all()
```

### 数据库连接安全
```python
# ❌ 错误：硬编码数据库凭证
DATABASE_URL = "postgresql://user:password@localhost/db"

# ✅ 正确：从环境变量读取
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

# ✅ 正确：使用连接池
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # 验证连接有效性
)
```

---

## Web 安全 [MUST]

### HTTPS 强制
```python
from flask import Flask, request, redirect

app = Flask(__name__)

# 强制 HTTPS
@app.before_request
def enforce_https():
    if not request.is_secure:
        return redirect(request.url.replace('http://', 'https://'), code=301)

# 或使用 Flask-Talisman
from flask_talisman import Talisman
Talisman(app, force_https=True)
```

### CSP 头部
```python
@app.after_request
def add_security_headers(response):
    # 内容安全策略
    csp = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.example.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self';"
    )
    response.headers['Content-Security-Policy'] = csp

    # 其他安全头部
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    return response
```

### CSRF 防护
```python
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)

@app.route('/api/data', methods=['POST'])
@csrf.exempt  # 仅在必要时禁用 CSRF
def api_data():
    # 对于 API，使用 token-based 认证
    pass
```

---

## 认证和授权 [MUST]

### 密码策略
```python
import re

def validate_password(password: str) -> bool:
    """验证密码强度"""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")

    if not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain uppercase letter")

    if not re.search(r'[a-z]', password):
        raise ValueError("Password must contain lowercase letter")

    if not re.search(r'\d', password):
        raise ValueError("Password must contain digit")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("Password must contain special character")

    return True
```

### JWT 认证
```python
import jwt
from datetime import datetime, timedelta
from functools import wraps

SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def create_token(user_id: int) -> str:
    """创建 JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token: str) -> dict:
    """验证 JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Missing token'}), 401

        if not token.startswith('Bearer '):
            return jsonify({'error': 'Invalid token format'}), 401

        token = token.split(' ')[1]

        try:
            payload = verify_token(token)
            request.user_id = payload['user_id']
        except ValueError as e:
            return jsonify({'error': str(e)}), 401

        return f(*args, **kwargs)
    return decorated
```

### 基于 RBAC 的授权
```python
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

def require_role(*allowed_roles):
    """角色检查装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, 'user_id'):
                return jsonify({'error': 'Not authenticated'}), 401

            user = User.query.get(request.user_id)
            if user.role not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator

@app.route('/admin/users')
@require_auth
@require_role(Role.ADMIN)
def admin_users():
    pass
```

---

## 密钥管理 [MUST]

### 环境变量
```python
# .env 文件（不要提交到 git）
DATABASE_URL=postgresql://user:password@localhost/db
SECRET_KEY=your-secret-key-here
API_KEY=your-api-key

# .gitignore
.env
.env.local
.env.*.local

# Python 代码
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set")
```

### 密钥轮换
```python
from datetime import datetime, timedelta

def should_rotate_key(last_rotation: datetime, interval_days: int = 90) -> bool:
    """检查是否需要轮换密钥"""
    return datetime.now() - last_rotation > timedelta(days=interval_days)

def rotate_api_key(user_id: int) -> str:
    """轮换 API 密钥"""
    # 1. 生成新密钥
    new_key = generate_secure_key()

    # 2. 保存新密钥（标记旧密钥为即将过期）
    user.api_key = new_key
    user.api_key_expires_at = datetime.now() + timedelta(days=7)
    db.commit()

    # 3. 通知用户更换密钥
    send_key_rotation_notification(user.email)

    return new_key
```

---

## 依赖安全 [MUST]

### Python 依赖审计
```bash
# 安装安全审计工具
pip install safety bandit

# 检查已知漏洞
safety check

# 安全代码检查
bandit -r ./src

# 检查过时的包
pip list --outdated
```

### 定期更新依赖
```bash
# 查看过期的包
pip list --outdated

# 更新特定包
pip install --upgrade package_name

# 使用 pip-tools 管理依赖
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

---

## 日志和监控 [SHOULD]

### 安全日志
```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def log_security_event(event_type: str, details: dict):
    """记录安全事件"""
    logger.warning(
        "Security Event: %s | User: %s | IP: %s | Details: %s",
        event_type,
        details.get('user_id', 'anonymous'),
        details.get('ip_address', 'unknown'),
        json.dumps(details)
    )

# 使用示例
log_security_event('failed_login', {
    'username': username,
    'ip_address': request.remote_addr,
    'user_agent': request.user_agent.string
})
```

### 异常登录检测
```python
from collections import defaultdict
from datetime import datetime, timedelta

failed_attempts = defaultdict(list)

def check_brute_force(username: str, ip_address: str) -> bool:
    """检查暴力破解尝试"""
    now = datetime.now()
    key = f"{username}:{ip_address}"

    # 清理旧记录（1小时前）
    failed_attempts[key] = [
        attempt for attempt in failed_attempts[key]
        if now - attempt < timedelta(hours=1)
    ]

    # 检查失败次数
    if len(failed_attempts[key]) >= 5:
        logger.warning(f"Possible brute force attack: {key}")
        return True

    failed_attempts[key].append(now)
    return False
```

---

## 安全检查清单

### 代码审查检查点
- [ ] 所有用户输入都已验证和清理
- [ ] 使用参数化查询或 ORM
- [ ] 密码使用 bcrypt/argon2 哈希
- [ ] 敏感数据未被记录
- [ ] 使用 HTTPS 和适当的头部
- [ ] 实施 CSRF 防护
- [ ] 实施 API 限流
- [ ] 密钥存储在环境变量中
- [ ] 文件上传经过验证
- [ ] 依赖已审计和更新

### 部署前检查
- [ ] 所有 .env 文件在 .gitignore 中
- [ ] 没有硬编码的密钥或凭证
- [ ] 启用了 HTTPS
- [ ] 配置了 CSP 头部
- [ ] 实施了日志记录
- [ ] 配置了错误监控
- [ ] 启用了备份
- [ ] 测试了恢复过程

---

## 安全工具

### Python
```bash
# 安全审计
pip install safety bandit semgrep

safety check
bandit -r ./src
semgrep --config=auto

# 依赖检查
pip install pip-audit
pip-audit
```

### 通用
```bash
# Git 密钥扫描
pip install truffleHog
trufflehog --regex --entropy=False /path/to/repo

# 密钥检测
pip install gitleaks
gitleaks detect --source /path/to/repo
```

---

**记住**: 安全是持续的过程，不是一次性的任务。定期审查、测试和更新安全措施。

