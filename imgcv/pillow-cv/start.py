from PIL import Image, ImageFilter

# im = Image.open('../res/use4.jpg')
#
# w, h = im.size
#
# print("原图像属性值：宽：%s, 高：%s" % (w, h))

# im.thumbnail((w/2, h/2))
#
# im.filter(ImageFilter.BLUR)
#
# # im.save('../res/blur.jpg', 'jpeg')
#
# im.rotate(28.61045966596522).show()


# im = Image.new('RGB', (200, 500), (0, 255, 0))
# im.show()


# dog1 = Image.open('../res/dog1.jpg').resize((1000, 750)).filter(ImageFilter.DETAIL)
# dog2 = Image.open('../res/dog2.jpg').resize((1000, 750))
#
# dog1.show()
# Image.blend(dog1, dog2, 0.8).show()


im = Image.open('../res/use8.png')

# im.filter(ImageFilter.SMOOTH).show()

# print(im.getdata())
# print(im.palette)