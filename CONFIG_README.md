# 配置文件使用说明

## 概述

本项目现在支持通过配置文件管理API信息和代理设置，使敏感信息不会硬编码在代码中，并且可以通过Git忽略规则保护这些敏感数据。

## 文件说明

### 配置文件

1. **`config.template.json`** - 配置文件模板
   - 包含所有可配置项的示例
   - 可以安全地提交到Git仓库
   - 新用户可以基于此文件创建自己的配置

2. **`config.json`** - 实际配置文件
   - 包含真实的API密钥和代理信息
   - **已在.gitignore中忽略，不会提交到Git**
   - 每个开发者需要自己创建此文件

### 配置管理模块

3. **`config_manager.py`** - 配置管理器
   - 负责加载和验证配置文件
   - 提供统一的配置访问接口
   - 支持配置验证和摘要显示

4. **`test_with_config.py`** - 使用配置文件的测试程序
   - 演示如何使用配置管理器
   - 通过配置文件加载API和代理信息
   - **已在.gitignore中忽略**

## 配置文件格式

```json
{
  "api": {
    "app_id": "your_app_id_here",
    "app_secret": "your_app_secret_here"
  },
  "proxy": {
    "enabled": true,
    "http_url": "http://proxy.example.com:port",
    "https_url": "http://proxy.example.com:port"
  },
  "settings": {
    "timeout": 30,
    "ignore_api_limit": true,
    "ignore_api_limit_wait": 0.5,
    "ignore_api_limit_retry": 3
  }
}
```

### 配置项说明

#### API配置 (`api`)
- `app_id`: 领星API的应用ID
- `app_secret`: 领星API的应用密钥

#### 代理配置 (`proxy`)
- `enabled`: 是否启用代理 (true/false)
- `http_url`: HTTP代理URL
- `https_url`: HTTPS代理URL (如果不存在，会使用http_url)

#### 设置配置 (`settings`)
- `timeout`: 请求超时时间（秒）
- `ignore_api_limit`: 是否忽略API限流
- `ignore_api_limit_wait`: 限流时等待时间（秒）
- `ignore_api_limit_retry`: 限流重试次数

## 使用方法

### 1. 创建配置文件

如果是新用户，请按照以下步骤：

```bash
# 复制模板文件
cp config.template.json config.json

# 编辑配置文件，填入真实信息
notepad config.json  # Windows
# 或
nano config.json     # Linux/Mac
```

### 2. 在代码中使用配置

```python
from config_manager import get_config_manager
from lingxingapi import API

async def test_api():
    # 加载配置
    config = get_config_manager()

    # 验证配置
    if not config.validate_config():
        print("配置验证失败")
        return

    # 使用配置创建API客户端
    async with API(
        app_id=config.app_id,
        app_secret=config.app_secret,
        timeout=config.timeout,
        proxy=config.proxy_url if config.proxy_enabled else None
    ) as api:
        # 使用API...
        sellers = await api.basic.Sellers()
        print(f"获取到 {len(sellers.data)} 个店铺")
```

### 3. 运行测试

```bash
# 测试配置管理器
python config_manager.py

# 运行使用配置的API测试
python test_with_config.py
```

## 安全注意事项

### ✅ 安全的做法
- ✅ 使用 `config.template.json` 作为模板
- ✅ 实际的 `config.json` 文件在 `.gitignore` 中
- ✅ 敏感信息只在本地存在
- ✅ 定期检查 `.gitignore` 规则

### ❌ 不安全的做法
- ❌ 不要将真实的 `config.json` 提交到Git
- ❌ 不要在代码中硬编码API密钥
- ❌ 不要将配置文件分享给他人
- ❌ 不要在日志中打印完整的配置信息

## Git忽略规则

以下文件已被添加到 `.gitignore` 中，不会被Git跟踪：

```
# Configuration files (sensitive data)
config.json
*.local.json
.env
.env.local
.env.*.local

# Test files with real credentials
test_library_with_proxy.py
test_with_config.py
```

## 故障排除

### 配置文件不存在
```
FileNotFoundError: 配置文件 config.json 不存在
```
**解决方案**: 从 `config.template.json` 复制并创建 `config.json`

### 配置格式错误
```
ValueError: 配置文件格式错误
```
**解决方案**: 检查JSON格式，确保所有括号和引号正确

### 配置验证失败
```
配置验证失败:
  - 缺少 app_id 配置
  - 缺少 app_secret 配置
```
**解决方案**: 按照错误提示补全相应的配置项

### 代理连接失败
```
ServerError: 领星 API 服务器无响应
```
**解决方案**:
1. 检查代理URL是否正确
2. 确认代理服务器是否可用
3. 检查网络连接

## 扩展配置

如需添加新的配置项：

1. 在 `config.template.json` 中添加示例
2. 在 `config_manager.py` 中添加对应的属性方法
3. 更新配置验证逻辑
4. 在使用代码中访问新配置项

## 示例：不同环境的配置

可以为不同环境创建不同的配置文件：

- `config.dev.json` - 开发环境
- `config.prod.json` - 生产环境
- `config.local.json` - 本地环境

然后在代码中指定配置文件：

```python
config = get_config_manager("config.dev.json")
```