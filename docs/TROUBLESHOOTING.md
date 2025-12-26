# 故障排查指南

## 目录
- [启动问题](#启动问题)
- [Cookie 问题](#cookie-问题)
- [数据获取问题](#数据获取问题)
- [网络问题](#网络问题)
- [性能问题](#性能问题)
- [文件权限问题](#文件权限问题)
- [依赖问题](#依赖问题)
- [日志分析](#日志分析)

---

## 启动问题

### 1. 服务启动失败

**症状**:
```
[ERROR] Service failed to start, please check error log
```

**排查步骤**:

1. **查看错误日志**
   ```bash
   cat logs/douk_downloader_error.log
   ```

2. **常见错误及解决方案**:

   **错误**: `ModuleNotFoundError: No module named 'xxx'`
   ```bash
   # 解决方案：安装依赖
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   **错误**: `Address already in use`
   ```bash
   # 解决方案：端口被占用
   # 查找占用进程
   lsof -i :5555
   # 或
   netstat -tulpn | grep 5555
   
   # 杀死进程
   kill -9 <PID>
   
   # 或修改端口
   nano src/custom/static.py
   # 修改 SERVER_PORT = 5555 为其他端口
   ```

   **错误**: `Permission denied`
   ```bash
   # 解决方案：权限问题
   chmod +x run_background.sh
   sudo chown -R $USER:$USER Volume
   ```

---

### 2. 虚拟环境问题

**症状**:
```
[ERROR] Virtual environment does not exist!
```

**解决方案**:
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

---

### 3. Python 版本问题

**症状**:
```
SyntaxError: invalid syntax
```

**排查**:
```bash
# 检查 Python 版本
python --version
# 或
python3 --version

# 应该是 3.12 或更高版本
```

**解决方案**:
```bash
# Ubuntu/Debian
sudo apt install python3.12 python3.12-venv

# 重新创建虚拟环境
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 4. 数据库权限问题

**症状**:
```
sqlite3.OperationalError: attempt to write a readonly database
```

**解决方案**:
```bash
# 修复 Volume 目录权限
sudo chown -R $USER:$USER Volume
chmod 755 Volume
chmod 644 Volume/DouK-Downloader.db
```

---

## Cookie 问题

### 1. Cookie 未读取

**症状**:
```
[Cookie] 未找到 Cookie 配置，请设置 Cookie 后重新运行程序
```

**排查步骤**:

1. **检查 cookies.txt 是否存在**
   ```bash
   ls -la cookies.txt
   ```

2. **检查文件内容**
   ```bash
   cat cookies.txt
   ```

3. **检查文件位置**
   ```bash
   # cookies.txt 应该在项目根目录
   # 与 main.py 同级
   pwd
   ls -la | grep -E "(cookies.txt|main.py)"
   ```

**解决方案**:
```bash
# 创建 cookies.txt
touch cookies.txt

# 编辑并粘贴 Cookie
nano cookies.txt

# 重启服务
./run_background.sh restart api
```

---

### 2. Cookie 格式错误

**症状**:
```
[WARNING] cookies.txt 文件内容格式无效，无法解析 Cookie
```

**排查**:
```bash
# 查看文件内容
cat -A cookies.txt

# 检查是否有多余的换行符、空格等
```

**正确格式**:
```
sessionid=xxx; sessionid_ss=xxx; sid_guard=xxx; uid_tt=xxx; ...
```

**常见错误**:
```
# 错误 1: 包含 "Cookie:" 前缀
Cookie: sessionid=xxx; ...

# 错误 2: 多行格式
sessionid=xxx
sessionid_ss=xxx

# 错误 3: 缺少分号
sessionid=xxx sessionid_ss=xxx
```

**解决方案**:
```bash
# 重新复制 Cookie，确保格式正确
# 删除所有多余字符
nano cookies.txt
```

---

### 3. Cookie 失效

**症状**:
```
配置文件 cookie 参数未登录，数据获取已提前结束
```

**原因**:
- Cookie 过期
- 账号退出登录
- 账号被限制

**解决方案**:
1. 重新登录抖音
2. 获取新 Cookie
3. 更新 cookies.txt
4. 重启服务

```bash
# 更新 Cookie
nano cookies.txt
# 粘贴新 Cookie

# 重启服务
./run_background.sh restart api

# 验证
curl -X POST "http://localhost:5555/douyin/account" \
  -H "Content-Type: application/json" \
  -d '{"sec_user_id": "xxx", "max_count": 1}'
```

---

### 4. Cookie 权限问题

**症状**:
```
Permission denied: 'cookies.txt'
```

**解决方案**:
```bash
# 修改文件权限
chmod 644 cookies.txt

# 或更安全的权限
chmod 600 cookies.txt

# 确保所有者正确
chown $USER:$USER cookies.txt
```

---

## 数据获取问题

### 1. 无法获取账号数据

**症状**:
```json
{
  "message": "获取数据失败！",
  "data": null
}
```

**排查步骤**:

1. **检查 sec_user_id 是否正确**
   ```bash
   # sec_user_id 应该是类似这样的格式：
   # MS4wLjABAAAAxxx...
   ```

2. **检查账号是否存在**
   - 访问账号主页确认账号存在
   - 确认账号不是私密账号

3. **检查 Cookie 状态**
   ```bash
   ./run_background.sh logs | grep Cookie
   ```

4. **查看详细错误**
   ```bash
   ./run_background.sh error-logs
   ```

---

### 2. 私密账号无法访问

**症状**:
```
该账号为私密账号，需要使用登录后的 Cookie，且登录的账号需要关注该私密账号
```

**解决方案**:
1. 使用已关注该账号的 Cookie
2. 或先关注该账号，再重新获取 Cookie

---

### 3. 数据不完整

**症状**:
- 只获取到部分作品
- count 参数不生效

**排查**:

1. **检查 max_count 参数**
   ```json
   {
     "sec_user_id": "xxx",
     "max_count": 20  // 确保设置了此参数
   }
   ```

2. **检查日志**
   ```bash
   ./run_background.sh logs | tail -50
   ```

3. **检查是否被限流**
   - 降低请求频率
   - 更换 IP 或使用代理

---

### 4. 重复检测不生效

**症状**:
- 提交相同 home_url 没有提示已存在

**排查**:
```bash
# 检查数据库
sqlite3 Volume/DouK-Downloader.db "SELECT * FROM mapping_data;"
```

**解决方案**:
- 确保使用的是 sec_user_id 而不是 URL
- 或确保 URL 格式正确

---

## 网络问题

### 1. 连接超时

**症状**:
```
TimeoutException: Request timeout
```

**解决方案**:

1. **增加超时时间**
   ```json
   // Volume/settings.json
   {
     "timeout": 30  // 增加到 30 秒
   }
   ```

2. **检查网络连接**
   ```bash
   ping www.douyin.com
   curl -I https://www.douyin.com
   ```

3. **使用代理**
   ```json
   {
     "proxy": "http://proxy-server:port"
   }
   ```

---

### 2. 代理问题

**症状**:
```
ProxyError: Cannot connect to proxy
```

**排查**:

1. **测试代理**
   ```bash
   curl -x http://proxy-server:port https://www.douyin.com
   ```

2. **检查代理格式**
   ```
   正确: http://proxy-server:port
   正确: socks5://proxy-server:port
   错误: proxy-server:port
   ```

3. **检查代理认证**
   ```
   http://username:password@proxy-server:port
   ```

---

### 3. DNS 解析失败

**症状**:
```
DNSError: Failed to resolve hostname
```

**解决方案**:
```bash
# 修改 DNS
sudo nano /etc/resolv.conf
# 添加
nameserver 8.8.8.8
nameserver 1.1.1.1

# 或使用 hosts 文件
sudo nano /etc/hosts
# 添加
xxx.xxx.xxx.xxx www.douyin.com
```

---

## 性能问题

### 1. 内存占用过高

**症状**:
- 系统内存不足
- 进程被 OOM Killer 杀死

**排查**:
```bash
# 查看内存使用
ps aux | grep python
top -p <PID>
```

**解决方案**:

1. **限制并发数**
   ```python
   # src/custom/static.py
   MAX_WORKERS = 2  # 减少并发数
   ```

2. **分批处理**
   ```json
   {
     "max_count": 50  // 减少单次获取数量
   }
   ```

---

### 2. CPU 占用过高

**症状**:
- CPU 使用率持续 100%

**排查**:
```bash
top
htop
```

**解决方案**:
1. 检查是否有死循环
2. 查看日志是否有异常
3. 重启服务

---

### 3. 响应速度慢

**症状**:
- API 响应时间过长

**优化方案**:

1. **使用更快的存储**
   - SSD 代替 HDD

2. **优化数据库**
   ```bash
   sqlite3 Volume/DouK-Downloader.db "VACUUM;"
   ```

3. **清理日志**
   ```bash
   # 清理旧日志
   > logs/douk_downloader.log
   > logs/douk_downloader_error.log
   ```

---

## 文件权限问题

### 1. 无法创建文件

**症状**:
```
PermissionError: [Errno 13] Permission denied
```

**解决方案**:
```bash
# 修复权限
sudo chown -R $USER:$USER .
chmod 755 .
chmod 755 Volume
chmod 755 logs
```

---

### 2. 无法写入数据库

**症状**:
```
sqlite3.OperationalError: attempt to write a readonly database
```

**解决方案**:
```bash
# 修复数据库权限
chmod 644 Volume/DouK-Downloader.db
chmod 755 Volume

# 确保所有者正确
chown $USER:$USER Volume/DouK-Downloader.db
```

---

## 依赖问题

### 1. 依赖安装失败

**症状**:
```
ERROR: Could not install packages
```

**解决方案**:

1. **使用国内镜像**
   ```bash
   pip install -r requirements.txt \
     -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. **更新 pip**
   ```bash
   pip install --upgrade pip
   ```

3. **逐个安装**
   ```bash
   # 查看失败的包
   cat requirements.txt | while read pkg; do
     pip install $pkg || echo "Failed: $pkg"
   done
   ```

---

### 2. 版本冲突

**症状**:
```
ERROR: Package has incompatible dependencies
```

**解决方案**:
```bash
# 删除虚拟环境重建
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 日志分析

### 查看日志的方法

1. **实时日志**
   ```bash
   ./run_background.sh follow
   ```

2. **最近日志**
   ```bash
   ./run_background.sh logs 100
   ```

3. **错误日志**
   ```bash
   ./run_background.sh error-logs
   ```

4. **搜索特定内容**
   ```bash
   grep "Cookie" logs/douk_downloader.log
   grep "ERROR" logs/douk_downloader_error.log
   ```

---

### 常见日志分析

#### 1. Cookie 相关
```bash
# 查看 Cookie 状态
grep -i "\[Cookie\]" logs/douk_downloader.log | tail -5
```

**正常输出**:
```
[Cookie] 读取成功: 已从 cookies.txt 文件读取抖音 Cookie 并应用到配置中
```

**异常输出**:
```
[Cookie] 未找到 Cookie 配置
[Cookie] cookies.txt 文件内容格式无效
```

#### 2. 请求相关
```bash
# 查看请求日志
grep -E "(开始处理|获取数据)" logs/douk_downloader.log | tail -10
```

#### 3. 错误统计
```bash
# 统计错误类型
grep "ERROR" logs/douk_downloader_error.log | \
  awk '{print $NF}' | sort | uniq -c | sort -rn
```

---

## 常用诊断命令

### 系统诊断
```bash
# 检查服务状态
./run_background.sh status

# 检查端口
netstat -tulpn | grep 5555
lsof -i :5555

# 检查进程
ps aux | grep python

# 检查磁盘空间
df -h

# 检查内存
free -h
```

### 文件诊断
```bash
# 检查关键文件
ls -la cookies.txt
ls -la Volume/settings.json
ls -la Volume/DouK-Downloader.db

# 检查文件权限
stat cookies.txt
stat Volume/DouK-Downloader.db

# 检查文件内容
head -1 cookies.txt
cat Volume/settings.json | jq '.cookie' | head -c 50
```

### 网络诊断
```bash
# 测试连接
curl -I https://www.douyin.com

# 测试 API
curl http://localhost:5555/

# 测试代理
curl -x http://proxy:port https://www.douyin.com
```

---

## 获取帮助

### 1. 查看文档
- [部署说明](./DEPLOYMENT.md)
- [API 使用说明](./API_USAGE.md)
- [Cookie 配置](./COOKIE_CONFIG.md)

### 2. 查看日志
```bash
# 完整日志
cat logs/douk_downloader.log
cat logs/douk_downloader_error.log
```

### 3. 提交 Issue
如果问题仍未解决，请提交 Issue 并包含：
- 问题描述
- 错误日志
- 系统信息
- 复现步骤

```bash
# 收集系统信息
echo "OS: $(uname -a)"
echo "Python: $(python --version)"
echo "Pip packages: $(pip list | grep -E '(httpx|fastapi|pydantic)')"
```

### 4. 社区支持
- GitHub Issues
- 项目文档
- QQ 群（见 README.md）

---

## 预防措施

### 1. 定期维护
```bash
# 每周执行
./run_background.sh restart api
sqlite3 Volume/DouK-Downloader.db "VACUUM;"
> logs/douk_downloader.log
```

### 2. 监控
```bash
# 设置监控脚本
cat > monitor.sh << 'EOF'
#!/bin/bash
if ! ./run_background.sh status > /dev/null 2>&1; then
    echo "Service down, restarting..."
    ./run_background.sh start api
fi
EOF

chmod +x monitor.sh

# 添加到 crontab
crontab -e
# 添加: */5 * * * * /path/to/monitor.sh
```

### 3. 备份
```bash
# 定期备份
tar -czf backup_$(date +%Y%m%d).tar.gz \
  Volume/DouK-Downloader.db \
  Volume/settings.json \
  cookies.txt
```

---

## 紧急恢复

### 完全重置
```bash
# 停止服务
./run_background.sh stop

# 备份数据
cp -r Volume Volume.backup
cp cookies.txt cookies.txt.backup

# 删除虚拟环境
rm -rf venv

# 重新部署
./setup_and_run.sh api
```

### 恢复备份
```bash
# 恢复数据库
cp Volume.backup/DouK-Downloader.db Volume/

# 恢复配置
cp Volume.backup/settings.json Volume/
cp cookies.txt.backup cookies.txt

# 重启服务
./run_background.sh restart api
```

