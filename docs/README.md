# DouK-Downloader 文档中心

欢迎使用 DouK-Downloader！这里是完整的文档导航。

---

## 📚 文档导航

### 🚀 快速开始
- **[快速入门指南](./QUICK_START.md)** - 5分钟快速上手
  - 安装部署
  - 第一个 API 请求
  - 常用功能示例

### 📦 部署相关
- **[部署说明](./DEPLOYMENT.md)** - 完整的部署指南
  - 系统要求
  - 详细部署步骤
  - Cookie 配置
  - 服务管理
  - 配置文件说明

### 🔧 使用指南
- **[API 使用说明](./API_USAGE.md)** - API 接口完整文档
  - API 概述
  - 抖音 API 接口
  - TikTok API 接口
  - 响应格式
  - 使用示例
  - 最佳实践

### 🍪 Cookie 配置
- **[Cookie 配置详解](./COOKIE_CONFIG.md)** - Cookie 配置完全指南
  - Cookie 简介
  - 获取 Cookie 的方法
  - 配置方式
  - 验证与更新
  - 安全建议

### 🔍 故障排查
- **[故障排查指南](./TROUBLESHOOTING.md)** - 常见问题解决方案
  - 启动问题
  - Cookie 问题
  - 数据获取问题
  - 网络问题
  - 性能问题
  - 日志分析

### 📖 其他文档
- **[Cookie 获取教程](./Cookie获取教程.md)** - 图文教程
- **[DouK-Downloader 文档](./DouK-Downloader文档.md)** - 原始文档
- **[Release Notes](./Release_Notes.md)** - 版本更新记录

---

## 🎯 按场景查找

### 我是新手，第一次使用
1. 阅读 [快速入门指南](./QUICK_START.md)
2. 按照 [部署说明](./DEPLOYMENT.md) 完成部署
3. 参考 [Cookie 配置详解](./COOKIE_CONFIG.md) 配置 Cookie
4. 查看 [API 使用说明](./API_USAGE.md) 开始使用

### 我遇到了问题
1. 查看 [故障排查指南](./TROUBLESHOOTING.md)
2. 检查日志文件
3. 搜索 GitHub Issues
4. 提交新 Issue

### 我想了解 API 接口
1. 访问 Swagger UI: `http://your-server:5555/docs`
2. 阅读 [API 使用说明](./API_USAGE.md)
3. 查看示例代码

### 我的 Cookie 有问题
1. 阅读 [Cookie 配置详解](./COOKIE_CONFIG.md)
2. 查看 [Cookie 获取教程](./Cookie获取教程.md)
3. 检查 [故障排查指南](./TROUBLESHOOTING.md) 中的 Cookie 问题部分

---

## 🆕 最新更新

### 新增功能
- ✅ 支持从 `cookies.txt` 文件读取 Cookie
- ✅ 添加 `max_count` 参数限制返回数量
- ✅ 添加 `sort` 参数支持排序（按时间/点赞数）
- ✅ 支持主页 URL 自动提取 sec_user_id
- ✅ 添加重复账号检测功能
- ✅ 启动时显示 Cookie 读取状态

### 配置优化
- Cookie 配置优先级：API 参数 > cookies.txt > settings.json
- 启动日志显示 Cookie 读取状态
- 优化错误提示信息

---

## 📋 功能特性

### 抖音平台
- ✅ 获取账号作品（发布/喜欢）
- ✅ 获取单个作品详情
- ✅ 获取合集作品
- ✅ 获取直播信息
- ✅ 获取作品评论
- ✅ 搜索功能（综合/视频/用户/直播）
- ✅ 批量操作支持
- ✅ 数量限制与排序

### TikTok 平台
- ✅ 获取账号作品
- ✅ 获取单个作品详情
- ✅ 获取合辑作品
- ✅ 获取直播信息

### 通用功能
- ✅ RESTful API 接口
- ✅ Swagger UI 文档
- ✅ 代理支持
- ✅ 自定义 Cookie
- ✅ 原始数据返回
- ✅ 详细错误信息

---

## 🔗 快速链接

### 在线资源
- **项目主页**: https://github.com/JoeanAmier/TikTokDownloader
- **问题反馈**: https://github.com/JoeanAmier/TikTokDownloader/issues
- **项目文档**: https://github.com/JoeanAmier/TikTokDownloader/wiki

### 本地资源
- **API 文档**: http://localhost:5555/docs
- **ReDoc**: http://localhost:5555/redoc
- **日志目录**: `logs/`
- **配置文件**: `Volume/settings.json`
- **Cookie 文件**: `cookies.txt`

---

## 📞 获取帮助

### 文档
- 优先查阅本文档中心的相关文档
- 查看 API 文档了解接口详情

### 社区
- GitHub Issues: 搜索或提交问题
- QQ 群: 见 README.md

### 日志
- 查看日志文件定位问题
- 使用 `./run_background.sh logs` 查看日志

---

## 🤝 贡献

欢迎贡献文档改进！

1. Fork 项目
2. 创建分支
3. 提交改进
4. 发起 Pull Request

---

## 📄 许可证

GNU General Public License v3.0

---

## 🙏 致谢

感谢所有贡献者和用户的支持！

---

**最后更新**: 2024-12-26

