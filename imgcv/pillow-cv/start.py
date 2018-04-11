from PIL import Image, ImageFilter


im = Image.open('../res/use4.jpg')

w, h = im.size

print("原图像属性值：宽：%s, 高：%s" % (w, h))

im.thumbnail((w/2, h/2))

im.filter(ImageFilter.BLUR)

# im.save('../res/blur.jpg', 'jpeg')

im.rotate(28.61045966596522).show()