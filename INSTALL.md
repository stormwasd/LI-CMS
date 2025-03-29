# LI-CMS 安装指南

本文档提供了LI-CMS内容管理系统的详细安装说明。

## 基础安装（推荐）

### 前提条件

- Python 3.7+
- pip 包管理器
- 可选：MySQL 数据库

### 步骤

1. **获取源码**

   ```bash
   git clone git@github.com:stormwasd/LI-CMS.git
   cd LI-CMS
   ```

2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

3. **数据库配置**

   执行以下命令生成数据库配置文件：

   ```bash
   python migrate.py
   ```

   这将在 `config/` 目录下创建 `database.py` 文件。

   **编辑配置文件：**
   
   - 默认情况下，LI-CMS使用SQLite数据库，无需额外配置
   - 如需使用MySQL，修改 `config/database.py` 中的以下内容：
     ```python
     # 修改数据库类型为mysql
     DB_TYPE = "mysql"
     
     # 更新MySQL配置
     MYSQL_CONFIG = {
         'host': 'localhost',     # 数据库服务器
         'port': 3306,            # 端口
         'database': 'li-cms',    # 数据库名称
         'user': 'your_user',     # 用户名
         'password': 'your_pass', # 密码
         'charset': 'utf8mb4'     # 编码（请勿修改）
     }
     ```

4. **初始化数据库**

   ```bash
   python migrate.py --init
   ```

   此命令将：
   - 创建所有必要的数据库表
   - 导入初始配置和示例内容
   - 创建默认管理员账户

5. **运行应用**

   ```bash
   python run.py
   ```

   应用将在 http://localhost:5000 启动。

   - 前台地址：http://localhost:5000
   - 后台地址：http://localhost:5000/admin
   - 默认管理员：用户名 `admin`，密码 `123456`

## 高级安装（使用Flask-Migrate）

如果您需要进行数据库版本控制和迁移管理，可以使用基于Flask-Migrate的工具。

1. **安装额外依赖**

   ```bash
   pip install flask-script
   ```

2. **初始化迁移环境**

   ```bash
   python manage.py db init
   ```

3. **创建迁移脚本**

   ```bash
   python manage.py db migrate -m "initial migration"
   ```

4. **应用迁移并初始化数据**

   ```bash
   python manage.py init
   ```

## 配置说明

### 数据库选择

- **SQLite**：适合个人博客或低流量网站，无需额外配置
- **MySQL**：适合高流量网站或需要更复杂查询的场景

### 生产环境部署

对于生产环境，建议：

1. 使用Gunicorn或uWSGI作为WSGI服务器
2. 配置反向代理（如Nginx）
3. 启用HTTPS
4. 禁用调试模式

示例Gunicorn启动命令：
```bash
gunicorn -w 4 -b 127.0.0.1:8000 'run:app'
```

## 故障排除

**问题：数据库初始化失败**

- 检查数据库连接信息是否正确
- 确保数据库用户有足够权限
- 查看应用日志获取详细错误信息

**问题：执行 `python migrate.py --init` 时出现"module 'init_db' has no attribute 'init_admin_user'"错误**

这是因为代码调用了不存在的函数。可以通过以下方法解决：

1. 使用最新版本的migrate.py文件
2. 或者手动运行初始化脚本：
   ```python
   python -c "import init_db; init_db.init_db()"
   ```

**问题：应用无法启动**

- 检查依赖是否正确安装
- 验证配置文件语法
- 确保端口未被占用

## 更多帮助

如需更多帮助，请参考：
- 提交问题：https://github.com/stormwasd/LI-CMS/issues