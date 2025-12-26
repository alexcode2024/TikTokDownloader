# .env Cookie 配置指南

## 概述

现在 Cookie 配置已改为从 `.env` 文件读取，这是一个更标准和安全的配置方式。

## 配置步骤

### 1. 创建 .env 文件

```bash
# 复制示例文件
cp .env.example .env

# 或手动创建
nano .env
```

### 2. 填入 Cookie

编辑 `.env` 文件，填入你的 Cookie：

```bash
# 抖音 Cookie（必需）
DOUYIN_COOKIE=your_douyin_cookie_here

# TikTok Cookie（可选）
TIKTOK_COOKIE=your_tiktok_cookie_here
```

### 3. 重启服务

```bash
./run_background.sh restart api
```

## 获取 Cookie

### 方法 1: 使用浏览器开发者工具

1. 打开抖音网页版：https://www.douyin.com
2. 按 `F12` 打开开发者工具
3. 切换到 `Network` (网络) 标签
4. 刷新页面
5. 点击任意请求
6. 在 `Headers` 中找到 `Cookie`
7. 复制完整的 Cookie 字符串

### 方法 2: 使用浏览器插件

推荐使用 "EditThisCookie" 或 "Cookie-Editor" 等浏览器插件。

## 配置优先级

1. **最高优先级**: `.env` 文件中的 `DOUYIN_COOKIE` 和 `TIKTOK_COOKIE`
2. **次优先级**: `Volume/settings.json` 中的 `cookie` 字段

如果 `.env` 文件中配置了 Cookie，将覆盖 `settings.json` 中的配置。

## .env 文件格式

```bash
# 注释以 # 开头
# 变量格式：KEY=VALUE
# 不需要引号（除非值中包含特殊字符）

# 抖音 Cookie
DOUYIN_COOKIE=ttwid=1%7C...; passport_csrf_token=...; ...

# TikTok Cookie
TIKTOK_COOKIE=tt_csrf_token=...; tt_chain_token=...
```

## 验证配置

启动服务后，检查日志：

```bash
./run_background.sh logs 20
```

应该看到类似输出：

```
已从 .env 文件读取抖音 Cookie 并应用到配置中
[Cookie] 读取成功: 已从 .env 文件读取抖音 Cookie 并应用到配置中
```

## 安全建议

### 1. 不要提交 .env 文件到 Git

```bash
# 确保 .gitignore 包含
echo ".env" >> .gitignore
```

### 2. 设置适当的文件权限

```bash
chmod 600 .env  # 只有所有者可读写
```

### 3. 定期更新 Cookie

- Cookie 可能会过期
- 建议定期更新（每 1-2 周）

### 4. 备份配置

```bash
# 备份 .env 文件（注意安全）
cp .env .env.backup
```

## 故障排查

### 问题 1: Cookie 未生效

**症状**: 日志显示 "未找到 Cookie 配置"

**解决方法**:
1. 检查 `.env` 文件是否在项目根目录
2. 检查 `.env` 文件中是否配置了 `DOUYIN_COOKIE`
3. 检查 Cookie 字符串是否完整（没有换行或多余空格）

```bash
# 查看 .env 文件内容
cat .env

# 检查 Cookie 是否有效
grep "DOUYIN_COOKIE=" .env
```

### 问题 2: .env 文件格式错误

**症状**: 服务启动失败或 Cookie 读取失败

**解决方法**:
1. 确保每行格式为 `KEY=VALUE`
2. 不要在 `=` 两边添加空格
3. Cookie 值不要用引号包裹（除非 Cookie 本身包含引号）

```bash
# 正确格式
DOUYIN_COOKIE=cookie_value_here

# 错误格式
DOUYIN_COOKIE = cookie_value_here  # = 两边有空格
DOUYIN_COOKIE="cookie_value_here"  # 不需要引号
```

### 问题 3: 权限问题

**症状**: 无法读取 .env 文件

**解决方法**:
```bash
# 设置正确的文件权限
chmod 600 .env

# 确保文件所有者正确
chown ubuntu:ubuntu .env
```

## 与 Docker 集成

### docker-compose.yml

```yaml
version: '3'
services:
  douk-downloader:
    image: douk-downloader:latest
    env_file:
      - .env
    ports:
      - "5555:5555"
```

### Docker Run

```bash
docker run -d \
  -e DOUYIN_COOKIE="${DOUYIN_COOKIE}" \
  -e TIKTOK_COOKIE="${TIKTOK_COOKIE}" \
  -p 5555:5555 \
  douk-downloader:latest
```

## 常见问题

**Q: 可以同时使用 .env 和 settings.json 吗？**

A: 可以。.env 中的配置会覆盖 settings.json 中的配置。

**Q: 如何切换回 settings.json？**

A: 删除或重命名 .env 文件，程序会自动使用 settings.json 中的配置。

**Q: .env 文件可以包含其他配置吗？**

A: 可以。你可以在 .env 中添加其他环境变量，但目前程序只读取 `DOUYIN_COOKIE` 和 `TIKTOK_COOKIE`。

## 完整示例

```bash
# .env 文件完整示例

# 抖音 Cookie（必需）
DOUYIN_COOKIE=ttwid=1%7C...; passport_csrf_token=...; passport_csrf_token_default=...; session_tlb_tag_bk=...; my_rd=2; download_guide=...; sid_guard=...; uid_tt=...; uid_tt_ss=...; sid_tt=...; sessionid=...; sessionid_ss=...

# TikTok Cookie（可选）
TIKTOK_COOKIE=tt_csrf_token=...; tt_chain_token=...
```

## 相关文档

- **README.md** - 项目主文档
- **API_USAGE.md** - API 使用文档

---

**更新时间**: 2025-12-27  
**版本**: V5.8 Beta  
**状态**: ✅ 已实现并测试

