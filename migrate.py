#!/usr/bin/env python
"""
LI-CMS数据库迁移和初始化脚本
作者：[LHJ]
日期：[2025-03-38]
"""
import os
import sys
import shutil
import argparse
from app import create_app, db

def setup_config():
    """设置数据库配置文件"""
    config_template = os.path.join('config', 'database.template.py')
    config_file = os.path.join('config', 'database.py')
    
    # 如果配置文件不存在，复制模板
    if not os.path.exists(config_file):
        if os.path.exists(config_template):
            shutil.copy(config_template, config_file)
            print("已创建数据库配置文件 config/database.py")
            print("请修改此文件以设置您的数据库连接信息")
            return False
        else:
            print("错误：未找到配置模板文件!")
            return False
    return True

def init_db():
    """初始化数据库表结构并导入初始化数据"""
    # 获取数据库类型
    from config.database import DB_TYPE
    from config.database import MYSQL_CONFIG
    
    # 删除数据库锁文件
    lock_file = 'li-cms_db.lock'
    if os.path.exists(lock_file):
        os.remove(lock_file)
        print(f"已删除数据库锁文件：{lock_file}")
    
    # 如果是MySQL数据库，先删除再重建
    if DB_TYPE == 'mysql':
        try:
            import pymysql
            print(f"正在删除并重建MySQL数据库: {MYSQL_CONFIG['database']}")
            conn = pymysql.connect(
                host=MYSQL_CONFIG['host'],
                port=MYSQL_CONFIG['port'],
                user=MYSQL_CONFIG['user'],
                password=MYSQL_CONFIG['password']
            )
            with conn.cursor() as cursor:
                cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_CONFIG['database']}")
                cursor.execute(
                    f"CREATE DATABASE {MYSQL_CONFIG['database']} "
                    f"CHARACTER SET utf8mb4 "
                    f"COLLATE utf8mb4_unicode_ci"
                )
                print(f"MySQL数据库 {MYSQL_CONFIG['database']} 已重建")
            conn.close()
        except Exception as e:
            print(f"警告：MySQL数据库重建失败 - {str(e)}")
            return
    
    # 如果是SQLite数据库，删除数据库文件
    elif DB_TYPE == 'sqlite':
        from config.database import SQLITE_CONFIG
        # 使用全局的os模块而不是重新导入
        db_path = os.path.join(SQLITE_CONFIG['path'], SQLITE_CONFIG['database'])
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"SQLite数据库文件已删除: {db_path}")
    
    try:
        # 强制重新加载init_db模块，确保使用最新版本
        if 'init_db' in sys.modules:
            del sys.modules['init_db']
        
        import init_db
        # 使用init_db模块的init_db函数，传入配置中设置的数据库类型
        init_db.init_db(
            db_type=DB_TYPE,
            admin_nickname='skyscraper',
            admin_email='2565706797@qq.com'
        )
        print("创建数据库和表结构并且初始数据已导入")
        
        # 验证管理员信息是否正确
        app = create_app()
        with app.app_context():
            from app.models import User
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print(f"\n管理员信息验证:")
                print(f"用户名: {admin.username}")
                print(f"昵称: {admin.nickname}")
                print(f"邮箱: {admin.email}")
            else:
                print("警告: 未找到管理员用户!")
    except Exception as e:
        print(f"警告：初始数据导入失败 - {str(e)}")
        print(f"错误详情: {e}")
        import traceback
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='LI-CMS数据库迁移和初始化工具')
    parser.add_argument('--init', action='store_true', help='初始化数据库')
    parser.add_argument('--reset-config', action='store_true', help='重置数据库配置文件')
    
    args = parser.parse_args()
    
    if args.reset_config:
        config_file = os.path.join('config', 'database.py')
        if os.path.exists(config_file):
            os.remove(config_file)
        print("数据库配置文件已重置")
        
    # 确保配置文件存在
    if not setup_config():
        return
        
    if args.init:
        # 确认操作
        confirm = input("警告：此操作将删除现有数据库并重新创建所有表及初始数据。确定要继续吗? (y/n): ")
        if confirm.lower() == 'y':
            init_db()
        else:
            print("操作已取消")
    
    # 没有任何参数时显示帮助信息
    if not (args.init or args.reset_config):
        parser.print_help()
    
if __name__ == '__main__':
    main() 