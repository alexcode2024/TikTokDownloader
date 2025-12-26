# DouK-Downloader 快速入门

## 5 分钟快速开始

### 步骤 1: 克隆项目 (30秒)
```bash
git clone https://github.com/JoeanAmier/TikTokDownloader.git
cd TikTokDownloader
```

### 步骤 2: 配置 Cookie (2分钟)

1. 访问 [抖音网页版](https://www.douyin.com/) 并登录
2. 按 `F12` 打开开发者工具
3. 切换到 `Network` 标签，刷新页面
4. 找到任意请求，复制 `Cookie` 字段内容
5. 创建并编辑 `cookies.txt`:
   ```bash
   nano cookies.txt
   # 粘贴 Cookie 内容
   # Ctrl+O 保存, Ctrl+X 退出
   ```

### 步骤 3: 一键启动 (2分钟)
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh api
```

### 步骤 4: 访问 API
打开浏览器访问: http://localhost:5555/docs

---

## 第一个 API 请求

### 使用浏览器（Swagger UI）
1. 访问 http://localhost:5555/docs
2. 找到 `POST /douyin/account`
3. 点击 "Try it out"
4. 填入参数：
   ```json
   {
     "sec_user_id": "MS4wLjABAAAAxxx",
     "max_count": 20
   }
   ```
5. 点击 "Execute"

### 使用 cURL
```bash
curl -X POST "http://localhost:5555/douyin/account" \
  -H "Content-Type: application/json" \
  -d '{
    "sec_user_id": "MS4wLjABAAAAxxx",
    "max_count": 20
  }'
```

### 使用 Python
```python
import requests

response = requests.post(
    "http://localhost:5555/douyin/account",
    json={
        "sec_user_id": "MS4wLjABAAAAxxx",
        "max_count": 20
    }
)

data = response.json()
print(f"获取到 {len(data['data'])} 个作品")
```

---

## 常用功能

### 1. 获取账号最新作品
```bash
curl -X POST "http://localhost:5555/douyin/account" \
  -H "Content-Type: application/json" \
  -d '{
    "sec_user_id": "MS4wLjABAAAAxxx",
    "max_count": 20,
    "sort": 0
  }'
```

### 2. 获取点赞最多的作品
```bash
curl -X POST "http://localhost:5555/douyin/account" \
  -H "Content-Type: application/json" \
  -d '{
    "sec_user_id": "MS4wLjABAAAAxxx",
    "max_count": 50,
    "sort": 1
  }'
```

### 3. 获取单个作品详情
```bash
curl -X POST "http://localhost:5555/douyin/detail" \
  -H "Content-Type: application/json" \
  -d '{
    "detail_id": "7123456789012345678"
  }'
```

### 4. 搜索用户
```bash
curl -X POST "http://localhost:5555/douyin/search/user" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "搜索关键词",
    "count": 10
  }'
```

---

## 服务管理

### 启动服务
```bash
./run_background.sh start api
```

### 停止服务
```bash
./run_background.sh stop
```

### 重启服务
```bash
./run_background.sh restart api
```

### 查看状态
```bash
./run_background.sh status
```

### 查看日志
```bash
./run_background.sh logs
./run_background.sh follow  # 实时日志
```

---

## 常见问题

### Q: Cookie 在哪里配置？
A: 在项目根目录创建 `cookies.txt` 文件，粘贴 Cookie 内容。

### Q: 如何获取 sec_user_id？
A: 访问用户主页，URL 中的 `user/` 后面的字符串就是 sec_user_id。
   例如: `https://www.douyin.com/user/MS4wLjABAAAAxxx`

### Q: 端口被占用怎么办？
A: 编辑 `src/custom/static.py`，修改 `SERVER_PORT = 5555` 为其他端口。

### Q: Cookie 失效怎么办？
A: 重新获取 Cookie，更新 `cookies.txt`，重启服务。

---

## 下一步

- 📖 [完整部署说明](./DEPLOYMENT.md)
- 🔧 [API 使用文档](./API_USAGE.md)
- 🍪 [Cookie 配置详解](./COOKIE_CONFIG.md)
- 🔍 [故障排查指南](./TROUBLESHOOTING.md)

---

## 获取帮助

- GitHub Issues: https://github.com/JoeanAmier/TikTokDownloader/issues
- 项目文档: https://github.com/JoeanAmier/TikTokDownloader/wiki
- API 文档: http://localhost:5555/docs

