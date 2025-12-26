# Cookie 配置详细说明

## 目录
- [Cookie 简介](#cookie-简介)
- [获取 Cookie 的方法](#获取-cookie-的方法)
- [Cookie 配置方式](#cookie-配置方式)
- [Cookie 验证](#cookie-验证)
- [Cookie 更新](#cookie-更新)
- [常见问题](#常见问题)

---

## Cookie 简介

### 什么是 Cookie？
Cookie 是网站存储在浏览器中的小型数据文件，用于识别用户身份和保持登录状态。

### 为什么需要 Cookie？
- 访问私密账号的作品
- 获取账号喜欢/收藏的作品
- 提高数据获取成功率
- 避免频繁请求被限制

### Cookie 的有效期
- 抖音 Cookie 通常有效期为 30-90 天
- 如果长时间不使用，Cookie 可能会失效
- 修改密码或退出登录会导致 Cookie 失效

---

## 获取 Cookie 的方法

### 方法 1: 浏览器开发者工具（推荐）⭐

#### Chrome / Edge / Firefox

1. **打开抖音网页版**
   - 访问: https://www.douyin.com/
   - 登录你的抖音账号

2. **打开开发者工具**
   - 按 `F12` 键
   - 或右键点击页面 → 选择"检查"

3. **切换到 Network 标签**
   - 点击顶部的 `Network` (网络) 标签
   - 如果没有看到请求，刷新页面（F5）

4. **查找请求**
   - 在请求列表中找到任意一个请求
   - 点击该请求

5. **复制 Cookie**
   - 在右侧面板找到 `Request Headers` (请求标头)
   - 找到 `Cookie:` 字段
   - 复制整行内容（不包括 `Cookie:` 这几个字）

**示例图示**:
```
Request Headers:
  Accept: */*
  Cookie: sessionid=xxx; sessionid_ss=xxx; sid_guard=xxx; uid_tt=xxx; ...
  User-Agent: Mozilla/5.0 ...
```

复制从 `sessionid` 开始到末尾的所有内容。

#### Safari

1. 打开 Safari → 偏好设置 → 高级
2. 勾选"在菜单栏中显示开发菜单"
3. 访问抖音并登录
4. 开发 → 显示网页检查器
5. 按照 Chrome 的步骤 3-5 操作

---

### 方法 2: 使用浏览器扩展

#### EditThisCookie (Chrome/Edge)

1. **安装扩展**
   - Chrome Web Store 搜索 "EditThisCookie"
   - 点击"添加到 Chrome"

2. **获取 Cookie**
   - 访问并登录抖音
   - 点击浏览器工具栏的 EditThisCookie 图标
   - 点击"导出" → 选择 "Netscape HTTP Cookie File"
   - 复制导出的内容

3. **转换格式**
   - 将导出的内容转换为 `key=value; key=value` 格式

---

### 方法 3: 使用程序内置功能

#### 从剪贴板读取

1. **获取 Cookie**
   - 按照方法 1 复制 Cookie 到剪贴板

2. **运行程序**
   ```bash
   source venv/bin/activate
   python main.py
   ```

3. **选择功能**
   - 选择: `1. 从剪贴板读取 Cookie (抖音)`
   - 程序会自动读取剪贴板内容并验证

#### 从浏览器读取（Windows）

1. **以管理员身份运行**
   ```bash
   # Windows: 右键 → 以管理员身份运行
   python main.py
   ```

2. **选择功能**
   - 选择: `2. 从浏览器读取 Cookie (抖音)`
   - 选择浏览器类型（Chrome/Edge/Firefox）
   - 程序会自动读取并保存

**注意**: 
- Windows 系统需要管理员权限才能读取 Chromium 系浏览器的 Cookie
- macOS/Linux 不需要特殊权限

#### 手动输入

1. **运行程序**
   ```bash
   python main.py
   ```

2. **选择功能**
   - 选择: `3. 手动输入 Cookie (抖音)`
   - 粘贴 Cookie 内容
   - 按回车确认

---

## Cookie 配置方式

### 方式 1: 使用 cookies.txt 文件（推荐）⭐

#### 优点
- ✅ 简单直接
- ✅ 易于更新
- ✅ 优先级最高
- ✅ 不影响配置文件

#### 配置步骤

1. **创建文件**
   ```bash
   cd /path/to/TikTokDownloader
   touch cookies.txt
   ```

2. **编辑文件**
   ```bash
   nano cookies.txt
   # 或使用其他编辑器
   ```

3. **粘贴 Cookie**
   ```
   sessionid=xxx; sessionid_ss=xxx; sid_guard=xxx; uid_tt=xxx; ...
   ```

4. **保存文件**
   - nano: `Ctrl+O` → `Enter` → `Ctrl+X`
   - vim: `:wq`

5. **设置权限（可选但推荐）**
   ```bash
   chmod 600 cookies.txt
   ```

#### 文件格式要求
- 纯文本格式
- 单行或多行均可
- 格式：`key1=value1; key2=value2; ...`
- 不要包含额外的空行或注释

**正确示例**:
```
sessionid=abc123; sessionid_ss=def456; sid_guard=ghi789; uid_tt=jkl012; ...
```

**错误示例**:
```
# 这是注释（错误！）
Cookie: sessionid=abc123; ...（错误！包含 "Cookie:" 前缀）

sessionid=abc123
（错误！缺少分号分隔）
```

---

### 方式 2: 配置 settings.json

#### 优点
- ✅ 集中管理所有配置
- ✅ 支持 JSON 格式
- ✅ 可以配置多个平台

#### 配置步骤

1. **编辑配置文件**
   ```bash
   cd /path/to/TikTokDownloader
   nano Volume/settings.json
   ```

2. **找到 cookie 字段**
   ```json
   {
     "cookie": "",
     "cookie_tiktok": "",
     ...
   }
   ```

3. **填入 Cookie**
   ```json
   {
     "cookie": "sessionid=xxx; sessionid_ss=xxx; sid_guard=xxx; ...",
     "cookie_tiktok": "sessionid=yyy; ...",
     ...
   }
   ```

4. **保存文件**

#### 注意事项
- Cookie 字符串需要用双引号包裹
- 特殊字符需要转义（通常不需要）
- 确保 JSON 格式正确

---

### 方式 3: API 请求时传入

#### 优点
- ✅ 灵活性高
- ✅ 支持多账号
- ✅ 临时使用

#### 使用方法

```bash
curl -X POST "http://localhost:5555/douyin/account" \
  -H "Content-Type: application/json" \
  -d '{
    "sec_user_id": "MS4wLjABAAAAxxx",
    "cookie": "sessionid=xxx; sessionid_ss=xxx; ...",
    "max_count": 20
  }'
```

#### Python 示例
```python
import requests

payload = {
    "sec_user_id": "MS4wLjABAAAAxxx",
    "cookie": "sessionid=xxx; sessionid_ss=xxx; ...",
    "max_count": 20
}

response = requests.post(
    "http://localhost:5555/douyin/account",
    json=payload
)
```

---

## Cookie 优先级

程序按以下优先级使用 Cookie：

1. **API 请求参数中的 cookie** （最高优先级）
2. **cookies.txt 文件**
3. **Volume/settings.json 中的 cookie 字段** （最低优先级）

### 优先级示例

如果同时存在：
- `cookies.txt`: `sessionid=aaa; ...`
- `settings.json`: `"cookie": "sessionid=bbb; ..."`
- API 请求: `"cookie": "sessionid=ccc; ..."`

则使用顺序：
1. API 请求中的 `sessionid=ccc`
2. 如果 API 未传，使用 cookies.txt 中的 `sessionid=aaa`
3. 如果 cookies.txt 不存在，使用 settings.json 中的 `sessionid=bbb`

---

## Cookie 验证

### 验证 Cookie 是否有效

#### 方法 1: 查看启动日志

启动服务后，查看日志：
```bash
./run_background.sh start api
```

输出示例：
```
[Cookie] 读取成功: 已从 cookies.txt 文件读取抖音 Cookie 并应用到配置中
```

#### 方法 2: 测试 API

```bash
curl -X POST "http://localhost:5555/douyin/account" \
  -H "Content-Type: application/json" \
  -d '{
    "sec_user_id": "MS4wLjABAAAAxxx",
    "max_count": 1
  }'
```

如果返回数据，说明 Cookie 有效。

#### 方法 3: 使用测试脚本

```bash
source venv/bin/activate
python test_token.py
```

### Cookie 必需字段

抖音 Cookie 必需包含以下字段之一：
- `sessionid` 或 `sessionid_ss`
- `sid_guard`
- `uid_tt`

**检查方法**:
```bash
grep -o "sessionid" cookies.txt
grep -o "sid_guard" cookies.txt
```

---

## Cookie 更新

### 何时需要更新 Cookie？

1. **Cookie 过期**
   - 错误提示：`cookie 参数未登录`
   - 获取数据失败

2. **账号密码修改**
   - 修改密码后立即失效

3. **长时间未使用**
   - 超过 30-90 天

4. **账号异常**
   - 被限制或封禁

### 更新步骤

#### 快速更新（推荐）

1. **获取新 Cookie**
   - 按照"获取 Cookie 的方法"重新获取

2. **更新 cookies.txt**
   ```bash
   nano cookies.txt
   # 粘贴新 Cookie
   # 保存退出
   ```

3. **重启服务**
   ```bash
   ./run_background.sh restart api
   ```

4. **验证**
   - 查看启动日志确认 Cookie 读取成功

#### 使用程序更新

```bash
source venv/bin/activate
python main.py
# 选择: 从剪贴板读取 Cookie (抖音)
```

程序会自动更新 `settings.json` 中的 Cookie。

---

## Cookie 安全

### 保护 Cookie

1. **设置文件权限**
   ```bash
   chmod 600 cookies.txt
   chmod 600 Volume/settings.json
   ```

2. **不要分享**
   - Cookie 等同于账号密码
   - 不要上传到公开仓库
   - 不要发送给他人

3. **添加到 .gitignore**
   ```bash
   echo "cookies.txt" >> .gitignore
   echo "Volume/settings.json" >> .gitignore
   ```

4. **定期更换**
   - 建议每月更换一次
   - 发现异常立即更换

### Cookie 泄露后的处理

1. **立即修改密码**
   - 登录抖音 → 设置 → 账号与安全 → 修改密码

2. **退出所有设备**
   - 设置 → 账号与安全 → 设备管理 → 退出所有设备

3. **更新 Cookie**
   - 重新登录获取新 Cookie
   - 更新配置文件

---

## 常见问题

### 1. Cookie 格式错误

**问题**: `cookies.txt 文件内容格式无效，无法解析 Cookie`

**原因**:
- Cookie 格式不正确
- 包含多余的字符或换行

**解决方案**:
```bash
# 检查文件内容
cat cookies.txt

# 确保格式为：
# key1=value1; key2=value2; ...
```

### 2. Cookie 未生效

**问题**: 配置了 Cookie 但仍提示未设置

**原因**:
- cookies.txt 文件位置错误
- 文件名拼写错误
- 文件编码问题

**解决方案**:
```bash
# 确认文件位置
ls -la cookies.txt

# 应该在项目根目录，与 main.py 同级
# 正确路径: /path/to/TikTokDownloader/cookies.txt
```

### 3. Cookie 快速失效

**问题**: Cookie 刚配置就失效

**原因**:
- 获取 Cookie 的账号已退出登录
- 浏览器清除了 Cookie
- 账号异常

**解决方案**:
1. 重新登录抖音
2. 不要在获取 Cookie 后退出登录
3. 使用常用设备和 IP 登录

### 4. 无法获取私密账号数据

**问题**: 提示"该账号为私密账号"

**原因**:
- 使用的 Cookie 对应的账号未关注该私密账号

**解决方案**:
1. 使用已关注该私密账号的账号 Cookie
2. 或先关注该账号，再获取 Cookie

### 5. Cookie 包含特殊字符

**问题**: Cookie 中有引号或其他特殊字符

**解决方案**:
- 在 cookies.txt 中直接粘贴，不需要转义
- 在 settings.json 中，双引号需要转义为 `\"`

**示例**:
```json
{
  "cookie": "key=\"value with quote\"; ..."
}
```

---

## TikTok Cookie 配置

### 获取 TikTok Cookie

方法与抖音类似，但需要：
1. 访问 https://www.tiktok.com/
2. 登录 TikTok 账号
3. 按照相同步骤获取 Cookie

### 配置 TikTok Cookie

#### cookies_tiktok.txt（如需支持）
```bash
touch cookies_tiktok.txt
nano cookies_tiktok.txt
# 粘贴 TikTok Cookie
```

#### settings.json
```json
{
  "cookie_tiktok": "sessionid=xxx; ...",
  ...
}
```

### TikTok 代理配置

TikTok 通常需要代理访问：
```json
{
  "proxy_tiktok": "http://proxy-server:port",
  ...
}
```

---

## 最佳实践

### 1. 使用专用账号
- 不要使用主账号
- 创建专门用于数据采集的账号
- 降低风险

### 2. 定期检查
```bash
# 每周检查一次 Cookie 状态
./run_background.sh status
./run_background.sh logs | grep Cookie
```

### 3. 备份 Cookie
```bash
# 备份当前 Cookie
cp cookies.txt cookies.txt.backup.$(date +%Y%m%d)
```

### 4. 监控日志
```bash
# 实时监控日志
./run_background.sh follow

# 查找 Cookie 相关日志
./run_background.sh logs | grep -i cookie
```

---

## 相关文档

- [部署说明](./DEPLOYMENT.md)
- [API 使用说明](./API_USAGE.md)
- [故障排查](./TROUBLESHOOTING.md)

