# PPress (二次开发版)

## 关于本二次开发版本

本项目LI-CMS是基于[原始PPress项目](https://gitee.com/fojie/PPress)的二次开发版本，在原有功能基础上进行了以下改进：

- 简化安装流程，支持通过配置文件直接配置数据库
- 添加数据库迁移工具，支持更灵活的数据库初始化
- 改进代码结构，优化用户体验
- 增强开发文档，方便二次开发

感谢原项目作者的贡献！

## 🌟 系统简介

LI-CMS 是一个基于 Flask 框架开发的功能丰富的博客内容管理系统（CMS）。它采用现代化的架构设计，提供流畅的博客写作和管理体验，适用于个人博客和内容驱动的网站。

### ✨ 核心特性

- **高性能设计**
  - 内存缓存机制
  - 缓存预热优化
  - 支持 SQLite 和 MySQL 数据库
  - 响应迅速的用户界面

- **完整的管理系统**
  - 文章管理
  - 分类管理
  - 页面管理
  - 用户管理
  - 评论系统
  - 系统配置
  - 模板管理
  - 插件系统

- **用户友好界面**
  - 清新现代的设计风格
  - 响应式布局
  - 直观的管理后台

## 🚀 快速开始

### 简化安装方法 (推荐)

1. **获取源码**
   ```bash
   git clone https://github.com/stormwasd/LI-CMS.git
   cd LI-CMS
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置数据库**
   ```bash
   # 生成数据库配置文件
   python migrate.py
   
   # 编辑配置文件
   # 根据需要修改 config/database.py 中的数据库设置
   # 默认使用SQLite，无需额外配置
   ```

4. **初始化数据库**
   ```bash
   # 创建数据库表并导入初始数据
   python migrate.py --init
   ```

5. **运行应用**
   ```bash
   python run.py
   ```

6. **访问应用**
   - 前台地址: http://localhost:5000
   - 后台地址: http://localhost:5000/admin
   - 默认管理员账号: admin / 123456

### 安装步骤

1. **获取源码**
   ```bash
   git clone https://github.com/stormwasd/LI-CMS.git
   cd LI-CMS
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**
   - 运行 `run.py`
   - 通过浏览器访问安装页面
   - 填写系统配置信息
   - 安装完成后重启应用

4. **访问后台**
   - 后台地址：`/admin/`
   - 默认管理员账号：
     - 用户名：`admin`
     - 密码：`123456`

## 🛠️ 技术栈

- **后端框架**: Flask
- **数据库**: SQLite/MySQL
- **缓存系统**: Flask-Caching
- **用户认证**: Flask-Login
- **数据库 ORM**: SQLAlchemy
- **模板引擎**: Jinja2
- **图像处理**: Pillow

## 📄 开源协议

LI-CMS 采用 [MIT 开源协议](LICENSE)。

### 关于二次开发协议说明

作为MIT协议的二次开发项目，本项目保留了原始协议的所有要求：

1. 本项目源自 [PPress](https://gitee.com/fojie/PPress)，原作者为 言道子
2. 原始版权声明和许可声明已保留在代码中
3. 本二次开发版本同样以MIT协议发布

## 🤝 参与贡献

我们欢迎各种形式的贡献：
- 报告问题和 Bug
- 提出新功能建议
- 提交代码改进

<div align="center">
    <p>由 LHJ用 ❤️ 打造</p>
</div>