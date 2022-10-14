#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import os
import sys
import argparse
import re

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops

TTF_FONT = os.path.dirname(__file__) + "/font/kuhei.ttf"

####function echo() start######
def echo( param,*args ):
    if len(args)==0:
        print(param)
    else:
        for var in args:
            if var=='':
                print(param,end='')
            else:
                print(param)
####function echo() end#######

def crop_image(im):
    '''裁剪图片边缘空白'''
    bg = Image.new(mode='RGBA', size=im.size)
    bbox = ImageChops.difference(im, bg).getbbox()
    if bbox:
        return im.crop(bbox)
    return im


def set_opacity(im, opacity):
    '''设置水印透明度'''
    assert 0 <= opacity <= 1
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def get_mark_img(text, color="#b7b7b7", size=30, opacity=0.15):
    """生成水印图片"""
    width = len(text) * size
    mark = Image.new(mode='RGBA', size=(width, size + 20))
    draw_table = ImageDraw.Draw(im=mark)
    draw_table.text(xy=(0, 0),
                    text=text,
                    fill=color,
                    font=ImageFont.truetype(TTF_FONT, size=size))
    del draw_table
    # 裁剪空白
    mark = crop_image(mark)
    # 透明度
    set_opacity(mark, opacity)
    return mark


def im_add_mark(im, text, color="#b7b7b7", size=30, opacity=0.15, space=75, angle=30):
    """给图片对象添加水印"""
    # 获取水印图片对象
    mark = get_mark_img(text, color, size, opacity)
    # 将水印图片扩展并旋转生成水印大图
    w, h = im.size
    c = int(math.sqrt(w ** 2 + h ** 2))
    mark2 = Image.new(mode='RGBA', size=(c, c))
    y, idx = 0, 0
    mark_w, mark_h = mark.size
    while y < c:
        x = -int((mark_w + space) * 0.5 * idx)
        idx = (idx + 1) % 2
        while x < c:
            mark2.paste(mark, (x, y))
            x = x + mark_w + space
        y = y + mark_h + space
    # 将水印大图旋转一定角度
    mark2 = mark2.rotate(angle)
    # 在原图上添加水印大图
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    im.paste(mark2, (int((w - c) / 2), int((h - c) / 2)),  # 坐标
             mask=mark2.split()[3])
    return im


def addTextMark2file(srcImageFile, text, out="output", color="#666666", size=30, opacity=0.15, space=75, angle=30):
    '''
    添加水印，然后保存图片
    '''
    name = os.path.basename(srcImageFile)
    pattern = re.compile(r'([\w]+\.(?:jpg|jpeg|png|bmp))', re.I | re.M)
    if pattern.search(out):
        new_name = out
    else:
        if not os.path.exists(out):
            os.makedirs(out)
        new_name = os.path.join(out, name)
    try:
        im = Image.open(srcImageFile)
        image = im_add_mark(im, text, color, size, opacity, space, angle)
        if os.path.splitext(new_name)[1] != '.png':
            image = image.convert('RGB')
        image.save(new_name)
        echo("Watermark added successfully!")
    except Exception as e:
        print(new_name, "保存失败。错误信息：", e)


def addTextMark(src, mark, out="output", color="#666666", size=30, opacity=0.15, space=75, angle=30):
    if os.path.isdir(src):
        names = os.listdir(src)
        for name in names:
            image_file = os.path.join(src, name)
            addTextMark2file(image_file, mark, out, color, size, opacity, space, angle)
    else:
        addTextMark2file(src, mark, out, color, size, opacity, space, angle)

############### help start ##########################
def _help():
    echo("使用方法: %s [选项]" % (sys.argv[0]))
    echo("选项有:")
    echo("    -h,--help \t :显示此帮助信息")
    echo("    -i,--src \t :需要添加水印的图片路径")
    echo("    -o,--out \t :输出的图片路径")
    echo("    -t,--txt \t :水印文字")
    echo("    -c,--color \t :水印文字颜色，默认是#666666")
    echo("    -s,--size \t :水印文字大小，默认是30")
    echo("    -p,--opacity \t :水印透明度，默认是0.15")
    echo("    -l,--space \t :行间距，默认是40")
    echo("    -r,--angle \t :旋转角度，默认是30")
    echo("    -f,--font \t :字体文件路径,默认为程序自带字体")
############### help end ##########################

def main():
    #创建参数解释器
    parser = argparse.ArgumentParser(description="图片添加水印工具")
    #添加预定的参数
    # parser.add_argument('-?', '--help')
    parser.add_argument('-i', '--src',required=True,help="需要添加水印的图片路径")
    parser.add_argument('-o', '--out',required=True,help="输出的图片路径")
    parser.add_argument('-t', '--txt',help="水印文字")
    parser.add_argument('-c', '--color', default="#666666",help="水印文字颜色，默认是#666666")
    parser.add_argument('-s','--size',metavar='int',type=int, default=30,help="水印文字大小，默认是30")
    parser.add_argument('-p','--opacity',type=float, default=0.15,help="水印透明度，默认是0.15")
    parser.add_argument('-l','--space',type=int, default=40,help="行间距，默认是40")
    parser.add_argument('-r','--angle',type=int, default=30,help="旋转角度，默认是30")
    parser.add_argument('-f', '--font',help="字体文件路径,默认为程序自带字体")
    #参数解析
    args = parser.parse_args()
    global TTF_FONT
    if args.font and os.path.exists(args.font):
        TTF_FONT = args.font
    if args.src == None or args.out == None or args.txt == None:
        _help()
    else:
        addTextMark(src=args.src,mark=args.txt, out=args.out,color=args.color, opacity=args.opacity, angle=args.angle, space=args.space)

if __name__ == "__main__":
    main()
