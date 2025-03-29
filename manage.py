#!/usr/bin/env python
"""
LI-CMS 数据库迁移管理工具 (基于 Flask-Migrate)
"""
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app, db
from config.database import DB_TYPE

# 初始化应用
app = create_app(init_components=False)
migrate = Migrate(app, db)
manager = Manager(app)

# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)

@manager.command
def init():
    """初始化数据库结构和基础数据"""
    # 执行数据库迁移
    os.system('python manage.py db upgrade')
    
    # 创建lockfile
    base_path = os.path.dirname(__file__)
    lock_file = os.path.join(base_path, 'li-cms_db.lock')
    with open(lock_file, 'w') as f:
        f.write('1')
    
    print("数据库结构已创建")
    
    # 导入初始数据
    with app.app_context():
        try:
            import init_db
            # 使用init_db模块的init_db函数
            init_db.init_db(db_type=DB_TYPE)
            print("初始数据已导入")
        except Exception as e:
            print(f"警告：初始数据导入失败 - {str(e)}")
            
    print("数据库初始化完成!")

@manager.command
def setup_config():
    """配置数据库连接"""
    from migrate import setup_config
    setup_config()
    
@manager.command
def reset_config():
    """重置数据库配置文件"""
    config_file = os.path.join('config', 'database.py')
    if os.path.exists(config_file):
        os.remove(config_file)
        print("数据库配置文件已重置")
    from migrate import setup_config
    setup_config()

if __name__ == '__main__':
    manager.run() 