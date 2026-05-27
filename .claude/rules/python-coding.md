# Python 编码规范 - MCLAUDE 项目

> **版本**: v1.1
> **最后更新**: 2025-03-26
> **来源**: 基于 MMCP 项目编码规范
> **适用**: MCLAUDE Python 项目

---

## 文件和目录命名 [MUST]

### Python 文件命名
- **规范**: 小写字母+下划线
- **正确示例**: `core_config_manager.py`, `cls_toolkit.py`, `get_data.py`
- **错误示例**: `CoreConfigManager.py`, `toolkit.py`, `GetData.py`

### 文档和配置文件命名
- **规范**: 小写字母+下划线
- **正确示例**: `project_context.md`, `coding_standards.md`, `integration_summary.md`
- **错误示例**: `PROJECT_CONTEXT.md`, `CodingStandards.md`, `INTEGRATION_SUMMARY.md`
- **标准例外**: `README.md` 保持大写（业界标准命名）

### 目录命名
- **规范**: 小写字母+下划线
- **正确示例**: `core/`, `ctk_class/`, `mcp_servers/`
- **错误示例**: `Core/`, `CTK_Class/`, `MCP_Servers/`

---

## 类、函数、变量命名 [MUST]

### 类命名 [大驼峰]
```python
# 正确
class MongoDBStorage:
class DependencyInjectionContainer:
class CustomButton(ctk.CTkButton):

# 错误
class mongoDB_storage:
class mongodbstorage:
```

### 函数命名 [小写+下划线]
```python
# 正确
def get_config_loader():
def create_demo_ui():
def update_user_profile():

# 错误
def GetConfigLoader():
def createDemoUI():
def update-user-profile():
```

### 变量命名 [小写+下划线]
```python
# 正确
user_name = "John"
private_var = "internal"
_max_connections = 100

# 错误
userName = "John"
PrivateVar = "internal"
maxConnections = 100
```

---

## 类型注解 [SHOULD]

### 基本要求
- **覆盖率**: 95%+ 的函数必须有类型注解
- **使用 typing 模块**: 使用 `typing` 模块的类型提示

### 示例
```python
from typing import List, Dict, Optional, Union, Callable, Any

# 函数签名
def get_user_list(user_id: int) -> List[Dict[str, Any]]:
    """获取用户列表"""
    pass

# 可选参数
def find_user(name: str, age: Optional[int] = None) -> Dict[str, Any]:
    """查找用户"""
    pass

# 联合类型
def process_data(data: Union[str, bytes]) -> str:
    """处理数据"""
    pass

# 回调函数
def on_complete(callback: Callable[[str], None]) -> None:
    """完成回调"""
    pass
```

---

## 文档字符串 [MUST]

### 函数文档字符串
```python
def calculate_metrics(data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    计算数据指标

    Args:
        data: 输入数据列表

    Returns:
        包含计算指标的字典，包含 avg, max, min 等键

    Raises:
        ValueError: 当数据为空时抛出
    """
    if not data:
        raise ValueError("数据不能为空")
    # 实现代码...
```

### 类文档字符串
```python
class MongoDBStorage:
    """
    MongoDB 存储管理器

    提供 MongoDB 数据库的连接、查询、更新等操作。

    Attributes:
        client: MongoDB 客户端实例
        db: 数据库实例

    Example:
        >>> storage = MongoDBStorage("mongodb://localhost:27017")
        >>> storage.connect()
        >>> data = storage.find("users", {"name": "John"})
    """
    def __init__(self, connection_string: str):
        """初始化 MongoDB 存储管理器"""
        self.client = None
        self.db = None
```


---

## 函数设计原则 [MUST]

### 函数长度
- **推荐**: 函数保持在 50 行以内
- **上限**: 不超过 100 行
- **原因**: 短函数更易理解、测试和维护

### 缩进层级
- **推荐**: 不超过 3 层缩进
- **上限**: 不超过 4 层缩进
- **处理**: 超过则需要重新设计，提取函数

### 单一职责
- 每个函数只做一件事
- 函数名应清晰描述其功能
- 避免多功能复合函数

---

## 代码质量 [MUST]

### 错误处理
```python
# 正确：具体的异常处理
try:
    result = database.query(query_string)
except DatabaseConnectionError as e:
    logger.error(f"数据库连接失败: {e}")
    raise
except DatabaseQueryError as e:
    logger.error(f"查询失败: {e}")
    return []

# 错误：过于宽泛的异常捕获
try:
    result = database.query(query_string)
except:
    pass
```

### 日志记录
```python
import logging

logger = logging.getLogger(__name__)

# 正确：使用适当的日志级别
logger.debug("调试信息")
logger.info("正常操作信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")

# 正确：包含上下文信息
logger.info(f"用户 {user_id} 登录成功，IP: {ip_address}")
logger.error(f"处理请求失败: {request_id}", exc_info=True)
```

---

## 导入顺序 [SHOULD]

### 标准顺序
```python
# 1. 标准库导入
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# 2. 第三方库导入
import pymongo
import customtkinter as ctk
from dotenv import load_dotenv

# 3. 本地模块导入
from core.core_config_manager import CoreConfigManager
from ctk_class.cls_toolkit import ClsToolkit
```

### 禁止的导入方式
```python
# 错误：通配符导入
from module import *

# 错误：不明确的导入
import package.module.submodule

# 正确：明确导入
from package.module import submodule
from package.module.submodule import specific_function
```

---

## 代码格式化 [SHOULD]

### 行长度
- **最大行长度**: 120 字符
- **推荐**: 80-100 字符

### 空行规则
```python
# 类定义之间：2个空行
class ClassA:
    pass


class ClassB:
    pass

# 方法定义之间：1个空行
class MyClass:
    def method1(self):
        pass

    def method2(self):
        pass
```

### 空格规则
```python
# 正确：运算符周围有空格
x = 1 + 2
result = func(a, b, c)

# 正确：逗号后有空格
function(arg1, arg2, arg3)

# 错误：多余的空格
x=1+2
result=func(a,b,c)
```

---

## 最佳实践 [SHOULD]

### 使用上下文管理器
```python
# 正确：使用 with 语句
with open("file.txt", "r") as f:
    content = f.read()

# 错误：手动管理资源
f = open("file.txt", "r")
content = f.read()
f.close()
```

### 列表推导式
```python
# 正确：简单的列表推导
squares = [x**2 for x in range(10)]

# 错误：过于复杂的列表推导
result = [x for x in items if x > 0 and x < 100 and x % 2 == 0]
# 应改为普通循环
result = [x for x in items if 0 < x < 100 if x % 2 == 0]
```

### 字符串格式化
```python
# 推荐：f-string（Python 3.6+）
name = "John"
greeting = f"Hello, {name}!"

# 可选：format()
greeting = "Hello, {}!".format(name)

# 避免：% 格式化
greeting = "Hello, %s!" % name
```

---

## 性能考虑 [MAY]

### 避免全局变量
```python
# 错误：使用全局变量
counter = 0

def increment():
    global counter
    counter += 1

# 正确：使用类或闭包
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
```

### 使用生成器处理大数据
```python
# 正确：使用生成器
def process_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield process_line(line)

# 错误：一次性加载所有数据
def process_large_file(filename):
    with open(filename) as f:
        lines = f.readlines()  # 可能占用大量内存
    return [process_line(line) for line in lines]
```

---

## 安全考虑 [MUST]

### 敏感信息处理
```python
# 错误：硬编码敏感信息
password = "mypassword"
api_key = "sk-1234567890"

# 正确：从环境变量读取
import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("DB_PASSWORD")
api_key = os.getenv("API_KEY")
```

### 输入验证
```python
# 正确：验证用户输入
def get_user_id(user_id: str) -> int:
    if not user_id.isdigit():
        raise ValueError("用户ID必须是数字")
    return int(user_id)

# 正确：使用白名单验证
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.png'}

def validate_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS
```

---

## 测试要求 [SHOULD]

### 单元测试
```python
import unittest

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config_manager = CoreConfigManager()

    def test_load_config(self):
        """测试配置加载"""
        config = self.config_manager.load_config("test_config.json")
        self.assertIsNotNone(config)
        self.assertIn("version", config)

    def test_invalid_config(self):
        """测试无效配置"""
        with self.assertRaises(ValueError):
            self.config_manager.load_config("invalid.json")
```

### 测试覆盖率
- **目标**: 80%+ 代码覆盖率
- **关键路径**: 100% 覆盖
- **工具**: pytest, coverage.py

---

## 代码格式化工具

### Black (格式化工具)
- **行长度**: 88 字符
- **目标版本**: Python 3.8+

### isort (导入排序)
- **配置**: 与 Black 兼容
- **自动排序**: 标准库 → 第三方 → 本地模块

### Pylint (代码检查)
- **配置文件**: .pylintrc
- **评分目标**: B 级别以上

### mypy (类型检查)
- **严格模式**: 可选
- **覆盖率**: 95%+ 类型注解

---

**注意**: 本规范基于 MMCP 项目编码规范，为 MCLAUDE 项目定制。
