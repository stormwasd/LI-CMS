#!/usr/bin/env python
"""
更新管理员用户信息
"""
from app import create_app, db
from app.models import User

def update_admin_info():
    """更新管理员信息"""
    app = create_app()
    
    with app.app_context():
        # 查找admin用户
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("找不到admin用户！")
            return
            
        print(f"当前admin用户信息:")
        print(f"用户名: {admin.username}")
        print(f"昵称: {admin.nickname}")
        print(f"邮箱: {admin.email}")
        
        # 更新信息
        admin.nickname = 'skyscraper'
        admin.email = '2565706797@qq.com'
        
        # 提交更改
        try:
            db.session.commit()
            print("\n更新成功!")
            print(f"新的admin用户信息:")
            print(f"用户名: {admin.username}")
            print(f"昵称: {admin.nickname}")
            print(f"邮箱: {admin.email}")
        except Exception as e:
            db.session.rollback()
            print(f"更新失败: {str(e)}")

if __name__ == '__main__':
    update_admin_info() 