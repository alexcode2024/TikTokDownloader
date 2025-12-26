# DouK-Downloader API 使用说明

## 目录
- [API 概述](#api-概述)
- [认证说明](#认证说明)
- [通用参数](#通用参数)
- [抖音 API](#抖音-api)
- [TikTok API](#tiktok-api)
- [响应格式](#响应格式)
- [错误处理](#错误处理)
- [使用示例](#使用示例)

---

## API 概述

### 基础信息
- **Base URL**: `http://your-server:5555`
- **API 文档**: 
  - Swagger UI: `http://your-server:5555/docs`
  - ReDoc: `http://your-server:5555/redoc`
- **Content-Type**: `application/json`
- **字符编码**: `UTF-8`

### API 特性
- ✅ RESTful 风格
- ✅ JSON 格式数据
- ✅ 支持代理配置
- ✅ 自动重试机制
- ✅ 详细错误信息
- ✅ 支持批量操作

---

## 认证说明

### Token 认证（可选）
默认情况下，API 不需要认证。如需启用认证，需修改 `src/custom/function.py` 中的 `is_valid_token()` 函数。

#### 启用认证后的使用方式
```bash
curl -X POST "http://your-server:5555/douyin/account" \
  -H "token: your-token-here" \
  -H "Content-Type: application/json" \
  -d '{"sec_user_id": "MS4wLjABAAAAxxx"}'
```

---

## 通用参数

### 可选参数（适用于大多数接口）

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `cookie` | string | 抖音/TikTok Cookie | 使用配置文件中的 Cookie |
| `proxy` | string | 代理地址 | null |
| `source` | boolean | 是否返回原始响应数据 | false |

### Cookie 参数说明
- 如果不传 `cookie` 参数，使用配置文件或 cookies.txt 中的 Cookie
- 传入 `cookie` 参数可以临时覆盖默认 Cookie
- Cookie 格式：`key1=value1; key2=value2; ...`

### Proxy 参数说明
支持的代理格式：
- HTTP: `http://proxy-server:port`
- HTTPS: `https://proxy-server:port`
- SOCKS5: `socks5://proxy-server:port`

---

## 抖音 API

### 1. 获取分享链接重定向地址

**接口**: `POST /douyin/share`

**说明**: 将抖音分享链接转换为完整链接

**请求参数**:
```json
{
  "text": "https://v.douyin.com/xxx/",
  "proxy": ""
}
```

**响应示例**:
```json
{
  "message": "请求链接成功！",
  "url": "https://www.douyin.com/video/7123456789012345678",
  "params": {
    "text": "https://v.douyin.com/xxx/",
    "proxy": ""
  }
}
```

---

### 2. 获取单个作品数据

**接口**: `POST /douyin/detail`

**说明**: 获取单个抖音作品的详细信息

**请求参数**:
```json
{
  "detail_id": "7123456789012345678",
  "cookie": "",
  "proxy": "",
  "source": false
}
```

**参数说明**:
- `detail_id` (必需): 作品 ID（19位数字）

**响应示例**:
```json
{
  "message": "获取数据成功！",
  "data": [
    {
      "id": "7123456789012345678",
      "desc": "作品描述",
      "create_time": "2024-01-01 12:00:00",
      "nickname": "用户昵称",
      "uid": "123456",
      "statistics": {
        "digg_count": 1000,
        "comment_count": 50,
        "share_count": 20
      },
      ...
    }
  ],
  "params": {...}
}
```

---

### 3. 获取账号作品数据 ⭐

**接口**: `POST /douyin/account`

**说明**: 获取抖音账号的发布/喜欢作品列表

**请求参数**:
```json
{
  "sec_user_id": "MS4wLjABAAAAxxx",
  "tab": "post",
  "earliest": "",
  "latest": "",
  "pages": null,
  "cursor": 0,
  "count": 18,
  "max_count": 20,
  "sort": 0,
  "cookie": "",
  "proxy": "",
  "source": false
}
```

**参数详解**:

| 参数 | 类型 | 说明 | 默认值 | 必需 |
|------|------|------|--------|------|
| `sec_user_id` | string | 账号 sec_uid 或主页 URL | - | ✅ |
| `tab` | string | 页面类型：`post`(发布) / `favorite`(喜欢) | `post` | ❌ |
| `earliest` | string | 最早发布日期（格式：YYYY/MM/DD） | - | ❌ |
| `latest` | string | 最晚发布日期（格式：YYYY/MM/DD） | 今天 | ❌ |
| `pages` | int | 最大请求次数（仅对喜欢页有效） | null | ❌ |
| `cursor` | int | 分页游标 | 0 | ❌ |
| `count` | int | 每次请求返回的作品数量 | 18 | ❌ |
| `max_count` | int | 最大返回作品总数量（null=不限制） | null | ❌ |
| `sort` | int | 排序方式：`0`=按发布日期倒序，`1`=按点赞数倒序 | 0 | ❌ |

**重要说明**:
- `sec_user_id` 可以传入账号主页 URL，程序会自动提取
- `count` 控制每次 API 请求的数量
- `max_count` 控制最终返回的总数量
- `sort=0` 按时间倒序（最新的在前）
- `sort=1` 按点赞数倒序（点赞最多的在前）

**使用示例**:

1. 获取最新 20 个作品：
```json
{
  "sec_user_id": "MS4wLjABAAAAxxx",
  "max_count": 20,
  "sort": 0
}
```

2. 获取点赞最多的 50 个作品：
```json
{
  "sec_user_id": "MS4wLjABAAAAxxx",
  "max_count": 50,
  "sort": 1
}
```

3. 使用主页 URL：
```json
{
  "sec_user_id": "https://www.douyin.com/user/MS4wLjABAAAAxxx",
  "max_count": 20
}
```

**响应示例**:
```json
{
  "message": "获取数据成功！",
  "data": [
    {
      "id": "7123456789012345678",
      "desc": "作品描述",
      "create_time": "2024-01-01 12:00:00",
      "nickname": "用户昵称",
      "statistics": {
        "digg_count": 5000,
        "comment_count": 200
      },
      ...
    }
  ],
  "params": {...}
}
```

---

### 4. 获取合集作品数据

**接口**: `POST /douyin/mix`

**说明**: 获取抖音合集的作品列表

**请求参数**:
```json
{
  "mix_id": "7123456789012345678",
  "detail_id": "",
  "cursor": 0,
  "count": 20,
  "cookie": "",
  "proxy": "",
  "source": false
}
```

**参数说明**:
- `mix_id` 和 `detail_id` 二选一
- `mix_id`: 合集 ID
- `detail_id`: 属于该合集的任意作品 ID

---

### 5. 获取直播数据

**接口**: `POST /douyin/live`

**说明**: 获取抖音直播间信息和拉流地址

**请求参数**:
```json
{
  "web_rid": "7123456789012345678",
  "cookie": "",
  "proxy": "",
  "source": false
}
```

**参数说明**:
- `web_rid`: 直播间 ID

**响应示例**:
```json
{
  "message": "获取数据成功！",
  "data": {
    "status": 2,
    "title": "直播标题",
    "nickname": "主播昵称",
    "flv_pull_url": "https://...",
    "hls_pull_url": "https://..."
  },
  "params": {...}
}
```

---

### 6. 获取作品评论数据

**接口**: `POST /douyin/comment`

**说明**: 获取抖音作品的评论列表

**请求参数**:
```json
{
  "detail_id": "7123456789012345678",
  "pages": 5,
  "cursor": 0,
  "count": 20,
  "count_reply": 3,
  "reply": false,
  "cookie": "",
  "proxy": "",
  "source": false
}
```

**参数说明**:
- `detail_id` (必需): 作品 ID
- `pages`: 最大请求次数
- `count`: 每次返回的评论数量
- `count_reply`: 每条评论返回的回复数量
- `reply`: 是否获取回复

---

### 7. 搜索功能

#### 综合搜索
**接口**: `POST /douyin/search/general`

#### 视频搜索
**接口**: `POST /douyin/search/video`

#### 用户搜索
**接口**: `POST /douyin/search/user`

#### 直播搜索
**接口**: `POST /douyin/search/live`

**通用请求参数**:
```json
{
  "keyword": "搜索关键词",
  "offset": 0,
  "count": 10,
  "pages": 1,
  "sort_type": 0,
  "publish_time": 0,
  "cookie": "",
  "proxy": "",
  "source": false
}
```

**参数说明**:
- `keyword` (必需): 搜索关键词
- `offset`: 起始页码
- `count`: 每页数量
- `pages`: 总页数
- `sort_type`: 排序类型（0=综合排序，1=最新发布，2=最多点赞）
- `publish_time`: 发布时间（0=不限，1=一天内，7=一周内，180=半年内）

---

## TikTok API

### 1. 获取分享链接重定向地址

**接口**: `POST /tiktok/share`

**请求参数**:
```json
{
  "text": "https://vm.tiktok.com/xxx/",
  "proxy": ""
}
```

---

### 2. 获取单个作品数据

**接口**: `POST /tiktok/detail`

**请求参数**:
```json
{
  "detail_id": "7123456789012345678",
  "cookie": "",
  "proxy": "",
  "source": false
}
```

---

### 3. 获取账号作品数据

**接口**: `POST /tiktok/account`

**请求参数**:
```json
{
  "sec_user_id": "MS4wLjABAAAAxxx",
  "tab": "post",
  "earliest": "",
  "latest": "",
  "pages": null,
  "cursor": 0,
  "count": 18,
  "max_count": 20,
  "sort": 0,
  "cookie": "",
  "proxy": "",
  "source": false
}
```

参数说明与抖音 API 相同。

---

### 4. 获取合辑作品数据

**接口**: `POST /tiktok/mix`

**请求参数**:
```json
{
  "mix_id": "7123456789012345678",
  "detail_id": "",
  "cursor": 0,
  "count": 20,
  "cookie": "",
  "proxy": "",
  "source": false
}
```

---

### 5. 获取直播数据

**接口**: `POST /tiktok/live`

**请求参数**:
```json
{
  "web_rid": "username",
  "cookie": "",
  "proxy": "",
  "source": false
}
```

---

## 响应格式

### 成功响应
```json
{
  "message": "获取数据成功！",
  "data": [...],  // 或 {...}
  "params": {
    // 请求参数的回显
  }
}
```

### 失败响应
```json
{
  "message": "获取数据失败！",
  "data": null,
  "params": {
    // 请求参数的回显
  }
}
```

### 字段说明
- `message`: 操作结果描述
- `data`: 返回的数据（数组或对象）
- `params`: 请求参数的回显

---

## 错误处理

### HTTP 状态码
- `200`: 请求成功
- `403`: Token 验证失败
- `422`: 参数验证失败
- `500`: 服务器内部错误

### 常见错误

#### 1. Cookie 失效
```json
{
  "message": "配置文件 cookie 参数未登录，数据获取已提前结束",
  "data": null
}
```
**解决方案**: 更新 Cookie

#### 2. 账号不存在或私密
```json
{
  "message": "该账号为私密账号，需要使用登录后的 Cookie...",
  "data": null
}
```
**解决方案**: 使用已登录且关注该账号的 Cookie

#### 3. 参数错误
```json
{
  "detail": [
    {
      "loc": ["body", "sec_user_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```
**解决方案**: 检查必需参数

---

## 使用示例

### Python 示例

```python
import requests

# API 基础地址
BASE_URL = "http://localhost:5555"

# 1. 获取账号最新 20 个作品
def get_account_posts():
    url = f"{BASE_URL}/douyin/account"
    payload = {
        "sec_user_id": "MS4wLjABAAAAxxx",
        "max_count": 20,
        "sort": 0
    }
    response = requests.post(url, json=payload)
    return response.json()

# 2. 获取点赞最多的 50 个作品
def get_top_liked_posts():
    url = f"{BASE_URL}/douyin/account"
    payload = {
        "sec_user_id": "MS4wLjABAAAAxxx",
        "max_count": 50,
        "sort": 1
    }
    response = requests.post(url, json=payload)
    return response.json()

# 3. 使用自定义 Cookie
def get_posts_with_cookie():
    url = f"{BASE_URL}/douyin/account"
    payload = {
        "sec_user_id": "MS4wLjABAAAAxxx",
        "max_count": 20,
        "cookie": "sessionid=xxx; sessionid_ss=xxx; ..."
    }
    response = requests.post(url, json=payload)
    return response.json()

# 4. 使用代理
def get_posts_with_proxy():
    url = f"{BASE_URL}/douyin/account"
    payload = {
        "sec_user_id": "MS4wLjABAAAAxxx",
        "max_count": 20,
        "proxy": "http://proxy-server:port"
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    result = get_account_posts()
    print(f"获取到 {len(result['data'])} 个作品")
```

### cURL 示例

```bash
# 1. 获取账号作品
curl -X POST "http://localhost:5555/douyin/account" \
  -H "Content-Type: application/json" \
  -d '{
    "sec_user_id": "MS4wLjABAAAAxxx",
    "max_count": 20,
    "sort": 0
  }'

# 2. 获取单个作品详情
curl -X POST "http://localhost:5555/douyin/detail" \
  -H "Content-Type: application/json" \
  -d '{
    "detail_id": "7123456789012345678"
  }'

# 3. 搜索用户
curl -X POST "http://localhost:5555/douyin/search/user" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "搜索关键词",
    "count": 10
  }'
```

### JavaScript 示例

```javascript
// 使用 fetch API
async function getAccountPosts() {
  const response = await fetch('http://localhost:5555/douyin/account', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      sec_user_id: 'MS4wLjABAAAAxxx',
      max_count: 20,
      sort: 0
    })
  });
  
  const data = await response.json();
  console.log(`获取到 ${data.data.length} 个作品`);
  return data;
}

// 使用 axios
const axios = require('axios');

async function getAccountPostsWithAxios() {
  try {
    const response = await axios.post('http://localhost:5555/douyin/account', {
      sec_user_id: 'MS4wLjABAAAAxxx',
      max_count: 20,
      sort: 0
    });
    console.log(`获取到 ${response.data.data.length} 个作品`);
    return response.data;
  } catch (error) {
    console.error('请求失败:', error.message);
  }
}
```

---

## 最佳实践

### 1. 错误处理
```python
def safe_api_call(url, payload):
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data') is None:
            print(f"获取数据失败: {data.get('message')}")
            return None
            
        return data
    except requests.exceptions.Timeout:
        print("请求超时")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    return None
```

### 2. 分页获取
```python
def get_all_posts(sec_user_id, batch_size=50):
    """分批获取所有作品"""
    all_posts = []
    cursor = 0
    
    while True:
        payload = {
            "sec_user_id": sec_user_id,
            "cursor": cursor,
            "count": 20,
            "max_count": batch_size
        }
        
        result = safe_api_call(f"{BASE_URL}/douyin/account", payload)
        if not result or not result['data']:
            break
            
        all_posts.extend(result['data'])
        
        if len(result['data']) < batch_size:
            break
            
        cursor += len(result['data'])
    
    return all_posts
```

### 3. 并发请求
```python
import concurrent.futures

def batch_get_posts(sec_user_ids):
    """批量获取多个账号的作品"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(get_account_posts, uid): uid 
            for uid in sec_user_ids
        }
        
        results = {}
        for future in concurrent.futures.as_completed(futures):
            uid = futures[future]
            try:
                results[uid] = future.result()
            except Exception as e:
                print(f"获取 {uid} 失败: {e}")
                
        return results
```

---

## 相关文档

- [部署说明](./DEPLOYMENT.md)
- [Cookie 配置](./COOKIE_CONFIG.md)
- [故障排查](./TROUBLESHOOTING.md)

