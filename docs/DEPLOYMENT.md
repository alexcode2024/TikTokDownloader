# DouK-Downloader 部署说明

## 目录
- [系统要求](#系统要求)
- [快速部署](#快速部署)
- [详细部署步骤](#详细部署步骤)
- [Cookie 配置](#cookie-配置)
- [服务管理](#服务管理)
- [配置文件说明](#配置文件说明)

---

## 系统要求

### 硬件要求
- CPU: 1核及以上
- 内存: 512MB及以上
- 磁盘: 1GB及以上可用空间

### 软件要求
- 操作系统: Linux (Ubuntu 20.04+推荐) / Windows / macOS
- Python: 3.12+
- Git: 用于克隆项目

---

## 快速部署

### 1. 克隆项目
```bash
git clone https://github.com/JoeanAmier/TikTokDownloader.git
cd TikTokDownloader
```

### 2. 一键安装并运行
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh api
```

该脚本会自动：
- 创建 Python 虚拟环境
- 安装所有依赖
- 启动 API 服务

---

## 详细部署步骤

### 步骤 1: 环境准备

#### Linux/macOS
```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
# 或
sudo yum update -y  # CentOS/RHEL

# 安装 Python 3.12+
sudo apt install python3.12 python3.12-venv python3-pip -y

# 安装 Git
sudo apt install git -y
```

#### Windows
1. 下载并安装 [Python 3.12+](https://www.python.org/downloads/)
2. 下载并安装 [Git](https://git-scm.com/download/win)
3. 确保在安装时勾选"Add Python to PATH"

### 步骤 2: 克隆项目
```bash
git clone https://github.com/JoeanAmier/TikTokDownloader.git
cd TikTokDownloader
```

### 步骤 3: 创建虚拟环境
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 步骤 4: 安装依赖
```bash
pip install -r requirements.txt
```

### 步骤 5: 配置 Cookie

#### 方式一：使用 cookies.txt 文件（推荐）
在项目根目录创建 `cookies.txt` 文件：
```bash
touch cookies.txt
```

将抖音 Cookie 粘贴到文件中：
```
sessionid=xxx; sessionid_ss=xxx; sid_guard=xxx; ...
```

#### 方式二：配置 settings.json
编辑 `Volume/settings.json` 文件，找到 `cookie` 字段并填入：
```json
{
  "cookie": "sessionid=xxx; sessionid_ss=xxx; sid_guard=xxx; ...",
  ...
}
```

> **注意**: 程序优先使用 `cookies.txt` 文件中的 Cookie

### 步骤 6: 启动服务

#### 前台运行（用于测试）
```bash
python main.py api
```

#### 后台运行（推荐）
```bash
chmod +x run_background.sh
./run_background.sh start api
```

---

## Cookie 配置

### 获取 Cookie 的方法

#### 方法 1: 浏览器开发者工具（推荐）
1. 打开浏览器，访问 [抖音网页版](https://www.douyin.com/)
2. 登录你的抖音账号
3. 按 `F12` 打开开发者工具
4. 切换到 `Network` (网络) 标签
5. 刷新页面
6. 找到任意请求，查看 `Request Headers`
7. 复制 `Cookie` 字段的完整内容

#### 方法 2: 使用程序内置功能
```bash
# 从剪贴板读取 Cookie
python main.py
# 选择: 从剪贴板读取 Cookie (抖音)

# 从浏览器读取 Cookie
python main.py
# 选择: 从浏览器读取 Cookie (抖音)
```

#### 方法 3: 手动输入
```bash
python main.py
# 选择: 手动输入 Cookie (抖音)
```

### Cookie 格式
Cookie 应该是以下格式：
```
key1=value1; key2=value2; key3=value3; ...
```

必需的关键字段：
- `sessionid` 或 `sessionid_ss`
- `sid_guard`
- `uid_tt`

### Cookie 配置优先级
1. **cookies.txt 文件**（最高优先级）
2. Volume/settings.json 中的 cookie 字段

---

## 服务管理

### 使用 run_background.sh 管理服务

#### 启动服务
```bash
./run_background.sh start api
```

输出示例：
```
[INFO] Starting service (mode: api)...
[SUCCESS] Service started successfully!
   PID: 12345
   Log: /path/to/logs/douk_downloader.log
   Error log: /path/to/logs/douk_downloader_error.log
   API URL: http://0.0.0.0:5555
   API Docs: http://0.0.0.0:5555/docs
   Cookie Status: [Cookie] 读取成功: 已从 cookies.txt 文件读取抖音 Cookie 并应用到配置中
```

#### 停止服务
```bash
./run_background.sh stop
```

#### 重启服务
```bash
./run_background.sh restart api
```

#### 查看服务状态
```bash
./run_background.sh status
```

#### 查看日志
```bash
# 查看最近 50 行日志
./run_background.sh logs

# 查看最近 100 行日志
./run_background.sh logs 100

# 实时跟踪日志
./run_background.sh follow
```

#### 查看错误日志
```bash
./run_background.sh error-logs
```

### 手动管理服务

#### 前台运行
```bash
source venv/bin/activate
python main.py api
```

#### 使用 nohup 后台运行
```bash
source venv/bin/activate
nohup python main.py api > logs/output.log 2>&1 &
```

#### 使用 systemd 管理（Linux）

创建服务文件 `/etc/systemd/system/douk-downloader.service`：
```ini
[Unit]
Description=DouK-Downloader API Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/TikTokDownloader
Environment="PATH=/path/to/TikTokDownloader/venv/bin"
ExecStart=/path/to/TikTokDownloader/venv/bin/python main.py api
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用并启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable douk-downloader
sudo systemctl start douk-downloader
sudo systemctl status douk-downloader
```

---

## 配置文件说明

### Volume/settings.json

主要配置项：

```json
{
  "cookie": "",                    // 抖音 Cookie（优先使用 cookies.txt）
  "cookie_tiktok": "",            // TikTok Cookie
  "root": "",                     // 下载文件保存根目录
  "folder_name": "Download",      // 下载文件夹名称
  "name_format": "create_time type nickname desc",  // 文件命名格式
  "download": true,               // 是否下载文件
  "max_size": 0,                  // 文件最大大小限制（0=不限制）
  "chunk": 2097152,               // 下载块大小（字节）
  "max_retry": 5,                 // 最大重试次数
  "timeout": 10,                  // 请求超时时间（秒）
  "proxy": "",                    // 代理设置
  "storage_format": "",           // 数据存储格式（csv/xlsx/sql）
  "douyin_platform": true,        // 是否启用抖音平台
  "tiktok_platform": true         // 是否启用 TikTok 平台
}
```

### cookies.txt

直接存放 Cookie 字符串，格式：
```
sessionid=xxx; sessionid_ss=xxx; sid_guard=xxx; uid_tt=xxx; ...
```

### src/custom/static.py

高级配置项：

```python
# 服务器监听地址
SERVER_HOST = "0.0.0.0"  # 0.0.0.0=对外开放，127.0.0.1=仅本地

# 服务器端口
SERVER_PORT = 5555

# 同时下载的最大任务数
MAX_WORKERS = 4

# Cookie 更新间隔（秒）
COOKIE_UPDATE_INTERVAL = 900  # 15分钟
```

---

## 访问 API

### API 文档
启动服务后，访问以下地址查看 API 文档：
- Swagger UI: `http://your-server:5555/docs`
- ReDoc: `http://your-server:5555/redoc`

### 修改监听地址
编辑 `src/custom/static.py`：
```python
SERVER_HOST = "0.0.0.0"  # 改为 "127.0.0.1" 仅本地访问
SERVER_PORT = 5555        # 修改端口号
```

---

## 常见问题

### 1. 权限问题
```bash
# 给予脚本执行权限
chmod +x run_background.sh setup_and_run.sh

# 修复 Volume 目录权限
sudo chown -R $USER:$USER Volume
```

### 2. 端口被占用
```bash
# 查看端口占用
lsof -i :5555
# 或
netstat -tulpn | grep 5555

# 修改端口（编辑 src/custom/static.py）
```

### 3. Cookie 失效
- 重新获取 Cookie 并更新 `cookies.txt` 文件
- 重启服务：`./run_background.sh restart api`

### 4. 依赖安装失败
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 安全建议

1. **不要公开暴露 API**
   - 使用防火墙限制访问
   - 配置 Nginx 反向代理
   - 启用 HTTPS

2. **保护 Cookie**
   - 不要分享 cookies.txt 文件
   - 定期更新 Cookie
   - 使用文件权限保护：`chmod 600 cookies.txt`

3. **定期更新**
   ```bash
   git pull
   pip install -r requirements.txt --upgrade
   ./run_background.sh restart api
   ```

---

## 下一步

- 查看 [API 使用说明](./API_USAGE.md)
- 查看 [Cookie 配置详解](./COOKIE_CONFIG.md)
- 查看 [故障排查指南](./TROUBLESHOOTING.md)

