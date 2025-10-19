# LingXing API - 领星ERP异步客户端

一个用于与领星(领星) ERP系统交互的异步Python客户端库。该库提供结构化接口，可访问各种领域特定API，包括基础数据、销售、FBA操作、产品、采购、仓库管理、广告、财务、工具和亚马逊源数据。

## 安装

### 从PyPI安装
```bash
pip install lingxingapi
```

### 从GitHub安装
```bash
pip install git+https://github.com/AresJef/LingXingApi.git
```

## 系统要求

- Python 3.10 或更高版本

## 快速开始

### 基本用法

```python
from lingxingapi import API

# 使用上下文管理器（推荐）
async def main():
    async with API(app_id, app_secret) as api:
        sellers = await api.basic.Sellers()
        print(f"获取到 {len(sellers.data)} 个店铺")

# 手动关闭会话
async def manual_example():
    api = API(app_id, app_secret)
    try:
        sellers = await api.basic.Sellers()
        print(f"获取到 {len(sellers.data)} 个店铺")
    finally:
        await api.close()
```

### 使用代理和自定义配置

```python
from lingxingapi import API

async def proxy_example():
    api = API(
        app_id="your_app_id",
        app_secret="your_app_secret",
        proxy="http://proxy.example.com:8080",  # 代理设置
        timeout=30,                             # 超时设置
        ignore_api_limit=True,                  # 自动处理限流
        ignore_api_limit_wait=0.5,              # 限流等待时间
        ignore_api_limit_retry=3                # 最大重试次数
    )

    async with api:
        marketplaces = await api.basic.Marketplaces()
        print(f"获取到 {len(marketplaces.data)} 个市场")
```

## API模块概览

### 基础数据 (api.basic)

| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `Marketplaces()` | 查询所有亚马逊站点信息 | 无 |
| `States(country_code)` | 查询指定国家的省/州信息 | `country_code`: 国家代码 (如 "US") |
| `Sellers()` | 查询所有店铺信息 | 无 |
| `ConceptSellers()` | 查询概念店铺列表 | 无 |
| `RenameSellers(*rename)` | 批量修改店铺名称 | `rename`: 店铺修改字典列表 |
| `Accounts()` | 查询ERP用户信息 | 无 |
| `ExchangeRates(start_date, end_date)` | 查询汇率信息 | `start_date`, `end_date`: 日期范围 |
| `EditExchangeRate(date, from_currency, to_currency, rate)` | 修改汇率 | `date`: 日期, `from_currency`, `to_currency`: 货币代码, `rate`: 汇率 |

### 销售数据 (api.sales)

#### Listing管理
| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `Listings(params)` | 查询亚马逊Listing | `sid`: 店铺ID, `search_field`: 搜索字段, `search_value`: 搜索值 |
| `EditListingOperators(*edit)` | 批量分配Listing负责人 | `edit`: 编辑字典列表 |
| `EditListingPrices(*edit)` | 批量修改Listing价格 | `edit`: 价格修改字典列表 |
| `PairListingProducts(*pair)` | 批量添加/编辑Listing配对 | `pair`: 配对字典列表 |
| `UnpairListingProducts(*unpair)` | 解除Listing配对 | `unpair`: 解除配对字典列表 |

#### 订单管理
| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `Orders(params)` | 查询亚马逊订单列表 | `sid`: 店铺ID, `start_date`, `end_date`: 日期范围 |
| `OrderDetails(*order_ids)` | 查询订单详情 | `order_ids`: 亚马逊订单ID列表 |
| `EditOrderNote(sid, order_id, note)` | 设置订单备注 | `sid`: 店铺ID, `order_id`: 订单ID, `note`: 备注 |
| `AfterSalesOrders(params)` | 查询售后订单列表 | `sid`: 店铺ID, `start_date`, `end_date`: 日期范围 |

### FBA数据 (api.fba)

| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `StaPlans(params)` | 查询STA任务列表 | `sid`: 店铺ID, `status`: 状态筛选 |
| `StaPlanDetail(plan_id)` | 查询STA任务详情 | `plan_id`: 任务ID |
| `PackingGroups(plan_id)` | 查询包装组 | `plan_id`: 任务ID |
| `Shipments(params)` | 查询货件列表 | `sid`: 店铺ID, `status`: 状态筛选 |
| `ShipmentDetails(shipment_id)` | 查询货件详情 | `shipment_id`: 货件ID |

### 产品数据 (api.product)

| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `Products(params)` | 查询本地产品列表 | `sid`: 店铺ID, `search_field`: 搜索字段 |
| `ProductDetails(*product_ids)` | 批量查询产品详情 | `product_ids`: 产品ID列表 |
| `EnableProducts(*product_ids)` | 启用产品 | `product_ids`: 产品ID列表 |
| `DisableProducts(*product_ids)` | 禁用产品 | `product_ids`: 产品ID列表 |
| `EditProduct(product_data)` | 添加/编辑本地产品 | `product_data`: 产品数据字典 |

### 采购数据 (api.purchase)

| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `Suppliers(params)` | 查询供应商列表 | `search_field`: 搜索字段, `search_value`: 搜索值 |
| `EditSupplier(supplier_data)` | 添加/修改供应商 | `supplier_data`: 供应商数据 |
| `Purchasers()` | 查询采购方列表 | 无 |
| `PurchasePlans(params)` | 查询采购计划列表 | `sid`: 店铺ID, `status`: 状态筛选 |

### 仓库数据 (api.warehouse)

| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `Warehouses()` | 查询仓库列表 | 无 |
| `WarehouseBins(warehouse_id)` | 查询仓位列表 | `warehouse_id`: 仓库ID |
| `FbaInventory(params)` | 查询FBA库存列表 | `sid`: 店铺ID, `warehouse_id`: 仓库ID |
| `SellerInventory(params)` | 查询库存明细 | `sid`: 店铺ID, `product_id`: 产品ID |

### 广告数据 (api.ads)

| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `AdProfiles(params)` | 查询广告账号列表 | `sid`: 店铺ID |
| `Portfolios(params)` | 查询广告组合 | `profile_id`: 广告账号ID |
| `SpCampaigns(params)` | 查询SP广告活动 | `profile_id`: 广告账号ID |
| `SpAdGroups(params)` | 查询SP广告组 | `campaign_id`: 广告活动ID |
| `SpKeywords(params)` | 查询SP关键词 | `ad_group_id`: 广告组ID |

### 财务数据 (api.finance)

| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `UserFeeTypes()` | 查询费用类型列表 | 无 |
| `Transactions(params)` | 查询交易明细 | `sid`: 店铺ID, `start_date`, `end_date`: 日期范围 |
| `Settlements(params)` | 查询结算汇总 | `sid`: 店铺ID, `start_date`, `end_date`: 日期范围 |
| `ShipmentSettlements(params)` | 查询发货结算报告 | `sid`: 店铺ID, `start_date`, `end_date`: 日期范围 |

### 工具数据 (api.tools)

| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `MonitorKeywords()` | 查询关键词列表 | 无 |
| `MonitorAsins(params)` | 查询竞品监控列表 | `search_field`: 搜索字段, `search_value`: 搜索值 |

### 亚马逊源数据 (api.source)

| 方法 | 描述 | 主要参数 |
|------|------|----------|
| `Orders(params)` | 查询所有订单 | `sid`: 店铺ID, `start_date`, `end_date`: 日期范围 |
| `FbaOrders(params)` | 查询FBA订单 | `sid`: 店铺ID, `start_date`, `end_date`: 日期范围 |
| `FbaInventory(params)` | 查询FBA库存 | `sid`: 店铺ID, `warehouse_id`: 仓库ID |
| `FbaInventoryHealth(params)` | 查询库龄表 | `sid`: 店铺ID |


## 高级功能

### 限流处理

```python
api = API(
    app_id, app_secret,
    ignore_api_limit=True,      # 自动重试限流错误
    ignore_api_limit_wait=0.2,  # 重试等待时间
    ignore_api_limit_retry=60   # 最大重试次数
)
```

### 分页查询

```python
async def paginated_example():
    async with API(app_id, app_secret) as api:
        # 查询第1页，每页50条记录
        listings = await api.sales.Listings({
            "sid": "123",
            "offset": 0,
            "length": 50
        })

        print(f"第1页: {len(listings.data)} 条记录")
```

### 批量操作

```python
async def batch_operations():
    async with API(app_id, app_secret) as api:
        # 批量修改价格
        price_edits = [
            {"sid": "123", "msku": "TEST001", "price": 19.99},
            {"sid": "123", "msku": "TEST002", "price": 29.99}
        ]
        result = await api.sales.EditListingPrices(*price_edits)
        print(f"修改结果: {result.message}")
```

## 错误处理

```python
from lingxingapi import errors

async def error_handling_example():
    try:
        async with API(app_id, app_secret) as api:
            sellers = await api.basic.Sellers()
    except errors.AccessTokenExpiredError:
        print("访问令牌已过期")
    except errors.ApiLimitError:
        print("API调用频率过高")
    except errors.ServerError as e:
        print(f"服务器错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
```

## 数据模型

### 常用响应结构

```python
# 店铺信息
class Seller:
    sid: int                    # 领星店铺ID
    seller_id: str             # 亚马逊卖家ID
    seller_name: str           # 店铺名称
    account_name: str          # 账户名
    marketplace_id: str        # 市场ID
    region: str               # 区域
    country: str              # 国家
    status: int               # 状态
    ads_authorized: int       # 广告授权状态

# 市场信息
class Marketplace:
    mid: int                  # 领星站点ID
    region: str              # 站点区域
    region_aws: str          # AWS区域
    country: str             # 国家
    country_code: str        # 国家代码
    marketplace_id: str      # 市场ID

# 订单信息
class Order:
    amazon_order_id: str     # 亚马逊订单ID
    seller_order_id: str     # 卖家订单ID
    purchase_date: str       # 购买日期
    order_status: str        # 订单状态
    fulfillment_channel: str # 配送渠道
    total_amount: float      # 订单总额
    currency: str           # 货币
```

## 接口文档

- [领星API官方文档](https://apidoc.lingxing.com/#/)
- 文档访问密钥: `hpvmgR4KeN`

## 开发指南

### 依赖项

- **aiohttp**: HTTP客户端，用于异步请求
- **pydantic**: 数据验证和解析
- **cytimes**: 时间工具
- **orjson**: 快速JSON解析
- **pycryptodome**: 加密操作
- **numpy**: 数值运算

### 项目结构

```
src/lingxingapi/
├── api.py              # 主API客户端
├── base/              # 基础API层
├── basic/             # 基础数据模块
├── sales/             # 销售数据模块
├── fba/               # FBA数据模块
├── product/           # 产品数据模块
├── purchase/          # 采购数据模块
├── warehouse/         # 仓库数据模块
├── ads/               # 广告数据模块
├── finance/           # 财务数据模块
├── tools/             # 工具数据模块
├── source/            # 亚马逊源数据模块
├── config_manager.py  # 配置管理器
└── errors.py          # 错误定义
```

## 许可证

MIT License

## 致谢

本项目基于以下开源库构建：

- [aiohttp](https://github.com/aio-libs/aiohttp) - 异步HTTP客户端
- [cytimes](https://github.com/AresJef/cyTimes) - 时间工具
- [numpy](https://github.com/numpy/numpy) - 数值计算
- [orjson](https://github.com/ijl/orjson) - 快速JSON解析
- [pydantic](https://github.com/pydantic/pydantic) - 数据验证