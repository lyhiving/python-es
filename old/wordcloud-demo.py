import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import PIL
import numpy as np

file_text = open("ci.txt", encoding='utf8').read()

dict_list = jieba.cut(file_text, cut_all=True)

di = " ".join(dict_list)

alice_img = np.array(PIL.Image.open("C:\\Users\\Administrator\\Desktop\\timg.jpg"))
wc = WordCloud(width=1920,
               height=1080,
               background_color="#fff",
               margin=2,
               mask=alice_img,
               font_path="C:\\Windows\\Fonts\\msyhbd.ttf")\
    .generate(di)

plt.imshow(wc)
plt.axis("off")
plt.show()
