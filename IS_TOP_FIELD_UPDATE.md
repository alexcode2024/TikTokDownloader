# is_top 字段更新说明

## 更新内容

在 `/douyin/account` 接口返回的简洁版数据中添加了 `is_top` 字段。

## 修改详情

### 修改文件
- `src/extract/extractor.py`

### 修改方法
1. `__extract_extra_info()` - 抖音数据提取
2. `__extract_extra_info_tiktok()` - TikTok 数据提取

### 代码变更

```python
def __extract_extra_info(self, item: dict, data: SimpleNamespace):
    if e := self.safe_extract(data, "anchor_info"):
        extra = dumps(e, ensure_ascii=False, indent=2, default=lambda x: vars(x))
    else:
        extra = ""
    item["extra"] = extra
    # 提取 is_top 字段（置顶标识）
    item["is_top"] = self.safe_extract(data, "is_top", 0)  # ✅ 新增
```

## 字段说明

### is_top

- **类型**: `int`
- **含义**: 作品是否置顶
- **取值**:
  - `0` - 未置顶
  - `1` - 已置顶
- **默认值**: `0`（如果原始数据中没有该字段）

## 使用示例

### 请求示例

```bash
curl -X POST "http://localhost:5555/douyin/account" \
  -H "Content-Type: application/json" \
  -d '{
    "sec_user_id": "MS4wLjABAAAA...",
    "source": false,
    "count": 20
  }'
```

### 响应示例（source: false）

```json
{
  "message": "数据获取成功",
  "data": [
    {
      "作品id": "7123456789",
      "作品描述": "这是一个置顶作品",
      "发布时间": "2023-12-20 10:00:00",
      "作者昵称": "用户昵称",
      "点赞数": 1000,
      "评论数": 50,
      "is_top": 1,  // ✅ 新增字段：表示该作品已置顶
      ...
    },
    {
      "作品id": "7123456790",
      "作品描述": "这是一个普通作品",
      "发布时间": "2023-12-19 10:00:00",
      "作者昵称": "用户昵称",
      "点赞数": 500,
      "评论数": 20,
      "is_top": 0,  // ✅ 新增字段：表示该作品未置顶
      ...
    }
  ]
}
```

### 响应示例（source: true）

原始数据中本来就包含 `is_top` 字段，无需额外处理：

```json
{
  "message": "数据获取成功",
  "data": [
    {
      "aweme_id": "7123456789",
      "desc": "这是一个置顶作品",
      "is_top": 1,  // ✅ 原始数据中的字段
      "create_time": 1703000000,
      "author": {...},
      "statistics": {...},
      ...
    }
  ]
}
```

## 应用场景

### 1. 筛选置顶作品

```python
# 获取账号数据
response = requests.post(
    "http://localhost:5555/douyin/account",
    json={
        "sec_user_id": "MS4wLjABAAAA...",
        "source": False
    }
)

data = response.json()["data"]

# 筛选置顶作品
top_works = [work for work in data if work.get("is_top") == 1]
print(f"置顶作品数量: {len(top_works)}")

# 筛选非置顶作品
normal_works = [work for work in data if work.get("is_top") == 0]
print(f"普通作品数量: {len(normal_works)}")
```

### 2. 按置顶状态排序

```python
# 置顶作品排在前面
sorted_data = sorted(data, key=lambda x: x.get("is_top", 0), reverse=True)
```

### 3. 显示置顶标识

```python
for work in data:
    title = work["作品描述"]
    if work.get("is_top") == 1:
        print(f"📌 [置顶] {title}")
    else:
        print(f"   {title}")
```

## 兼容性

### 向后兼容
- ✅ 不影响现有代码
- ✅ 如果不使用该字段，可以忽略
- ✅ 默认值为 `0`，不会导致错误

### 数据源
- ✅ 抖音（Douyin）：支持
- ✅ TikTok：支持（如果原始数据中有该字段）

## 测试验证

### 测试步骤

1. **启动服务**
```bash
./run_background.sh restart api
```

2. **调用 API（简洁版）**
```bash
curl -X POST "http://localhost:5555/douyin/account" \
  -H "Content-Type: application/json" \
  -d '{
    "sec_user_id": "MS4wLjABAAAA...",
    "source": false,
    "count": 10
  }'
```

3. **验证响应**
- 检查返回的数据中是否包含 `is_top` 字段
- 验证置顶作品的 `is_top` 值为 `1`
- 验证普通作品的 `is_top` 值为 `0`

### 预期结果

- ✅ 简洁版数据（`source: false`）包含 `is_top` 字段
- ✅ 详细版数据（`source: true`）保持原样
- ✅ 服务运行正常，无错误

## 技术细节

### 提取位置

`is_top` 字段在 `__extract_extra_info()` 方法中提取，该方法在批量处理作品数据时被调用：

```
__extract_batch()
  ├─> __extract_detail_info()      # 基本信息
  ├─> __extract_account_info()     # 账号信息
  ├─> __extract_music()            # 音乐信息
  ├─> __extract_statistics()       # 统计信息
  ├─> __extract_tags()             # 标签信息
  ├─> __extract_extra_info()       # 额外信息 ✅ is_top 在这里提取
  └─> __extract_additional_info()  # 附加信息
```

### 数据流程

```
原始数据 (source: true)
  ↓
  包含 is_top 字段
  ↓
Extractor.run()
  ↓
__extract_extra_info()
  ↓
提取 is_top 字段
  ↓
简洁数据 (source: false)
  ↓
包含 is_top 字段 ✅
```

## 相关文档

- **API_USAGE.md** - API 完整使用文档
- **ENV_COOKIE_GUIDE.md** - Cookie 配置指南

---

**更新时间**: 2025-12-27  
**版本**: V5.8 Beta  
**状态**: ✅ 已实现并测试

