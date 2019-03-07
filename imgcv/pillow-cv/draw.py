from PIL import Image, ImageDraw


im = Image.new('RGB', (1000, 750), (255, 255, 255))
draw = ImageDraw.Draw(im)
# 线条
# draw.line((im.size[0]/2, 0, im.size[0]/2, im.size[1]) + im.size, fill=(0, 0, 0))
# draw.line((0, im.size[1]/2, im.size[0], im.size[1]/2) + im.size, fill=(0, 0, 0))
# 矩形
# draw.ellipse((im.size[0]/2, 0) + im.size, fill=(0, 255, 0))
# 像素点
# draw.point([(10, 10)], fill=(0, 255, 0))
# 文字
draw.text((10, 10), 'hello', fill=(0, 255, 0))
del draw
# write to stdout

im.show()