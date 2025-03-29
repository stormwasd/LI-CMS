import base64
import os

from slugify import slugify

from app import create_app, db
from app.models import User, Article, Tag, Category, SiteConfig
from datetime import datetime
import pymysql
from config.database import MYSQL_CONFIG

LOCK_FILE = 'li-cms_db.lock'
COPYRIGHT_INFO = base64.b64decode(
    'UFByZXNzIC0gRmxhc2sgQ29udGVudCBNYW5hZ2VtZW50IFN5c3RlbQrniYjmnYPmiYDmnIkgKGMpIDIwMjQg6KiA6YGT5a2QCuS9nOiAhVFR77yaNTc1NzMyNTYzCumhueebruWcsOWdgO+8mmh0dHBzOi8vZ2l0ZWUuY29tL2ZvamllL1BQcmVzcw=='
).decode('utf-8')

def check_db_lock():
    """检查数据库锁"""
    if os.path.exists(LOCK_FILE):
        print("\n检测到数据库锁文件！这是为了防止意外重置数据库的安全机制！")
        print(f"如果确定要重新初始化数据库，请先删除以下文件：{os.path.abspath(LOCK_FILE)}")
        return True
    return False

def create_db_lock():
    """创建数据库锁文件"""
    with open(LOCK_FILE, 'w', encoding='utf-8') as f:
        f.write(COPYRIGHT_INFO)
    print(f"\n已创建数据库锁文件：{os.path.abspath(LOCK_FILE)}")

def update_db_config(db_type):
    """更新数据库配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'database.py')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式替换 DB_TYPE
        import re
        new_content = re.sub(
            r'DB_TYPE\s*=\s*["\'].*["\']',
            f'DB_TYPE = "{db_type}"',
            content
        )
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"\n数据库配置已更新：DB_TYPE = {db_type}")
        
    except Exception as e:
        print(f"\n更新数据库配置失败：{str(e)}")

def init_db(db_type='mysql', site_name='LI-CMS', admin_nickname='skyscraper', admin_email='2565706797@qq.com'):
    """初始化数据库
    Args:
        db_type (str): 数据库类型 'mysql' 或 'sqlite'
        site_name (str): 网站名称
        admin_nickname (str): 管理员昵称
        admin_email (str): 管理员邮箱
    """
    # 检查数据库锁
    if check_db_lock():
        return

    if db_type == 'mysql':
        # 使用配置文件中的连接信息
        conn = pymysql.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute('DROP DATABASE IF EXISTS ' + MYSQL_CONFIG['database'])
                cursor.execute(
                    f"CREATE DATABASE {MYSQL_CONFIG['database']} "
                    'CHARACTER SET utf8mb4 '
                    'COLLATE utf8mb4_unicode_ci'
                )
        finally:
            conn.close()

    # 创建应用实例，禁用所有组件初始化
    app = create_app(db_type=db_type, init_components=False)
    
    # 临时移除需要访问数据库的上下文处理器
    original_processors = app.context_processor
    app.context_processor = lambda: {}

    with app.app_context():
        print(f"\n开始初始化纯净数据到 {db_type} 数据库...")
        db.drop_all()
        db.create_all()
        
        # 初始化网站配置,传入自定义网站名称
        custom_configs = {
            'site_name': site_name,
            'footer_text': f'© 2025 {site_name} 版权所有'
        }
        SiteConfig.init_default_configs(custom_configs)
        
        # 创建管理员用户
        admin = User(
            username='admin',
            nickname=admin_nickname,
            email=admin_email,
            role='admin'
        )
        admin.set_password('123456')
        db.session.add(admin)
        
        # 创建一个标签
        tag = Tag(name='LI-CMS')
        db.session.add(tag)
        
        # 创建一个分类
        category = Category(
            name='示例分类',
            slug=slugify('示例分类'),  # 添加 slug
            description='LI-CMS 示例分类',
            sort_order=1  # 添加排序
        )

        db.session.add(category)
        
        # 提交以获取ID
        db.session.commit()
        
        # 创建一篇示例文章
        article = Article(
            title='欢迎使用 LI-CMS',
            content='''<p>欢迎使用 LI-CMS 博客系统！&nbsp;LI-CMS 是一个基于 Flask 的轻量级博客系统，由言道子开发(PPress)并由LHJ进行二开。</p>
<p>主要特点： 简洁优雅的界面设计、支持插件扩展、支持主题切换、完善的后台管理&nbsp;</p>
<p>项目地址：<a href="https://github.com/stormwasd/LI-CMS"</a></p>
<p>开始使用：</p>
<p>1. 使用管理员账号登录(admin/123456)</p>
<p>2. 在后台进行相关配置</p>
<p>3. 开始创作你的第一篇文章 如有问题或建议，欢迎联系作者！</p>''',
            author_id=admin.id,
            category_id=category.id,
            created_at=datetime.now(),
            view_count=0,
        )
        article.tags.append(tag)
        article.categories = [category]
        db.session.add(article)
        
        # 最终提交
        db.session.commit()
        
        print("纯净数据库初始化完成！")
        print("管理员账号：")
        print("用户名：admin")
        print("密码：123456")

        # 创建数据库锁文件
        create_db_lock()
        
        # 更新数据库配置
        update_db_config(db_type)
        
        # 恢复原始上下文处理器
        app.context_processor = original_processors

def get_db_type():
    """交互式获取数据库类型"""
    while True:
        choice = input("\n如果选mysql请提前在config/database.py中，把MYSQL_CONFIG配置好\n请选择数据库类型 [1/2]:\n1. SQLite (默认)\n2. MySQL\n请输入(直接回车使用SQLite，请输入1或者2): ").strip()

        if choice == '':
            print("\n已选择: SQLite")
            return 'sqlite'
        elif choice == '1':
            print("\n已选择: SQLite")
            return 'sqlite'
        elif choice == '2':
            print("\n已选择: MySQL")
            return 'mysql'
        else:
            print("\n输入无效,请重新选择")

if __name__ == '__main__':
    db_type = get_db_type()
    init_db(db_type)