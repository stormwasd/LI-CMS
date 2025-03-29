#!/usr/bin/env python
"""
生成带有L字母的favicon图标
"""
from PIL import Image, ImageDraw, ImageFont
import os

def generate_favicon():
    """生成带有L字母的favicon图标，圆形背景，字母居中"""
    # 创建一个透明背景的图像
    img = Image.new('RGBA', (32, 32), color=(0, 0, 0, 0))  # 透明背景
    
    # 创建画板
    draw = ImageDraw.Draw(img)
    
    # 绘制蓝色圆形背景
    circle_color = (1, 128, 255, 255)  # 蓝色
    draw.ellipse((0, 0, 31, 31), fill=circle_color)  # 画一个填充圆形
    
    try:
        # 尝试加载粗体字体
        try:
            # 尝试加载Arial Bold
            font = ImageFont.truetype("Arial Bold", 20)
        except:
            # 尝试加载Arial，但增加大小以显得更粗
            font = ImageFont.truetype("Arial", 22)
    except IOError:
        # 如果无法加载系统字体，使用默认字体
        font = ImageFont.load_default()
    
    # 计算文字居中位置 - 由于字母L较窄，手动调整位置
    position = (10, 4)  # 经过调整的位置，使字母L在圆中居中
    
    # 在图像中央绘制字母L
    draw.text(position, "L", font=font, fill=(255, 255, 255, 255))  # 白色字母
    
    # 创建稍微偏移的重叠文本以增加粗体效果
    draw.text((position[0]+1, position[1]), "L", font=font, fill=(255, 255, 255, 255))
    
    # 保存为.ico文件
    img.save('app/static/favicon.ico', format='ICO')
    
    print(f"新图标已生成并保存到: app/static/favicon.ico")
    print("请刷新浏览器或清除缓存以查看新图标")

if __name__ == "__main__":
    generate_favicon() 