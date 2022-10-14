# 图片添加水印
## 默认安装路径
建议安装路径为：/usr/local/watermark
将本watermark目录复制到/usr/local/下即可

## 环境安装
1. 安装python3环境;
2. 安装依赖：

```
cd /usr/local/watermark
pip3 install -r requirements.txt
```

## 参数
```
选项有:
    -h,--help 		 :显示帮助信息
    -i,--src 		 :需要添加水印的图片路径
    -o,--out 		 :输出的图片路径
    -t,--txt 		 :水印文字
    -c,--color 		 :水印文字颜色，默认是#666666
    -s,--size 		 :水印文字大小，默认是30
    -p,--opacity	 :水印透明度，默认是0.15
    -l,--space 		 :行间距，默认是40
    -r,--angle 		 :旋转角度，默认是30
    -f,--font 		 :字体文件路径,默认为程序自带字体
    
    -m,--mode		 :水印模式，枚举：txt,img
    -w,--watermark 	 :水印图片路径
    -g,--genre 		 :水印图片方式，overflow铺满，single单个
    -a,--position 	 :水印图片位置,c[中间],t[顶部中间],l[左边中间],r[右边中间],b[底部中间],rt[右上角],lt[左上角],rb[右下角],lb[左下角],默认rb
```


## 使用示例

```
python3 /usr/local/watermark/mywatermark.py \
-i /opt/demo.jpg \
-o /opt/demo_mark.jpg \
-t "仅限XXX使用，其他用途无效" \
-c "#b7b7b7"
```
## 参数资料

参考了filestools库的水印功能，filestools的水印功能在项目中不能完全满足需求，于是乎就改造了下,算是站在巨人的肩膀上了，哈哈。
