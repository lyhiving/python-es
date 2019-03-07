import requests
import logging
from bs4 import BeautifulSoup
import urllib
from contextlib import closing
import hashlib
import uuid
from pymongo import MongoClient

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')

page_request_list = 'https://www.yiten.net/m/ceramic/ShowDesign.ashx?API' \
                    '=MXw1NjI1fDU2MHwyNUY5RTc5NDMyM0I0NTM4ODVGNTE4MUYxQjYyNEQwQnlpdGlhbjU2MA==&width=214&Page=1' \
                    '&ClassID=5625&DesignClass=0&DesignStyle=0&temp=1551749789973 '

headers = {
    'host': 'www.yiten.net',
    'referer': 'https://www.yiten.net'
}

base_url = 'https://www.yiten.net/m/ceramic/'


conn = MongoClient('127.0.0.1', 27017)
db = conn.cj
mg_img = db.img
mg_records = db.records


def get_page_list():
    res = requests.get(url=page_request_list, headers=headers)
    if res.status_code == 200:
        logging.info('网页获取成功：%s', page_request_list)
        res_content = urllib.parse.unquote(res.content.decode())
        res_content = res_content.replace("falsefalse|", "")
        soup = BeautifulSoup(res_content)
        designContent = soup.find_all('li')
        if designContent is not None and len(designContent) > 0:
            dc720_list = []
            for dc in designContent:
                dc_href = dc.find('a')
                if dc_href is not None:
                    dc_href_src = dc_href.attrs['href']
                    if dc_href_src is not None:
                        if dc_href_src.startswith("Ceramic720"):
                            dc720_list.append(dc_href_src)
            # 进行分析抓取
            index = 1
            for dc720_item in dc720_list:
                logging.info("正在抓取第%d个全景：%s", index, dc720_item)
                parse_720_page(dc720_item)
                index = index + 1
        else:
            logging.error('全景列表为空：%s', page_request_list)
    else:
        logging.error('网页获取失败：%s', page_request_list)


def parse_720_page(url):
    res = requests.get(url=base_url + url, headers=headers)
    if res.status_code == 200:
        logging.info('720全景网页获取成功：%s', url)
        soup = BeautifulSoup(res.content.decode())
        wallleftString = soup.find('input', id='WallleftString')
        wallrightString = soup.find('input', id='WallrightString')
        wallcenterString = soup.find('input', id='WallcenterString')
        wallfloorString = soup.find('input', id='WallfloorString')

        # 抓取定位数据
        wallleftString_value = get_attr(wallleftString, 'value')
        wallleftString_res, lefts = get_params(wallleftString_value)

        wallrightString_value = get_attr(wallrightString, 'value')
        wallrightString_res, rights = get_params(wallrightString_value)

        wallcenterString_value = get_attr(wallcenterString, 'value')
        wallcenterString_res, centers = get_params(wallcenterString_value)

        wallfloorString_value = get_attr(wallfloorString, 'value')
        wallfloorString_res, floors = get_params(wallfloorString_value)

        # 抓取图片资源
        ImgSrc = get_attr(soup.find('input', id='ImgSrc'), 'value')
        Inverted = get_attr(soup.find('input', id='Inverted'), 'value')
        ObjShadow = get_attr(soup.find('input', id='ObjShadow'), 'value')
        LightShadow = get_attr(soup.find('input', id='LightShadow'), 'value')

        # 抓取封面图
        wx_pic = get_attr(soup.find('img', id='wx_pic'), 'src')

        res = {'left': parse_download_img(lefts), 'right': parse_download_img(rights),
               'center': parse_download_img(centers), 'floor': parse_download_img(floors),
               'imgSrc': parse_download_img(ImgSrc), 'inverted': parse_download_img(Inverted),
               'objShadow': parse_download_img(ObjShadow), 'lightShadow': parse_download_img(LightShadow),
               'wallLeftString': wallleftString_res, 'wallRightString': wallrightString_res,
               'wallCenterString': wallcenterString_res, 'wallFloorString': wallfloorString_res,
               'cover': download_img(wx_pic, True), 'wideangle': get_attr(soup.find('input', id='wideangle'), 'value'),
               'lookAtX': get_attr(soup.find('input', id='lookAtX'), 'value'),
               'lookAtY': get_attr(soup.find('input', id='lookAtY'), 'value'),
               'lookAtZ': get_attr(soup.find('input', id='lookAtZ'), 'value'),
               'positionX': get_attr(soup.find('input', id='positionX'), 'value'),
               'positionY': get_attr(soup.find('input', id='positionY'), 'value'),
               'positionZ': get_attr(soup.find('input', id='positionZ'), 'value')}

        # 抓取瓷砖位置数据

        mg_records.insert(res)
    else:
        logging.error('720全景网页获取失败：%s', url)


def get_attr(el, name):
    try:
        res = el.attrs[name]
    except KeyError as e:
        res = None
    return res


def get_params(str):
    if str is None or str.strip() == '':
        return None, None
    res_str = str
    fs = str.split("|")
    if fs is None or len(fs) == 0:
        return None, None
    imgs = []
    for fs_item in fs:
        ts = fs_item.split(",")
        if ts is None or len(ts) == 0:
            continue
        for ts_item in ts:
            if ts_item.startswith("/UploadFiles"):
                imgs.append(ts_item)
    if len(imgs) > 0:
        for img_item in imgs:
            res_str = res_str.replace(img_item, '%img%')
    return res_str, imgs


def parse_download_img(img):
    if img is None:
        return
    if type(img) == list and len(img) > 0:
        res = []
        for img_item in img:
            res.append(download_img(img_item))
        return res
    else:
        return download_img(img)


def download_img(path, has_base_url=False):
    if has_base_url:
        url = path
    else:
        url = 'https://www.yiten.net' + path
    result = mg_img.find_one({'origin': url})
    if result is not None:
        return result['path']
    ps = path.split(".")
    suffix = ps[len(ps)-1]
    file_name = hashlib.md5(uuid.uuid1().bytes).hexdigest()+'.'+suffix
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        data_count = 0
        with open('G:/cj/c2/'+file_name, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, url), end=" ")
    mg_img.insert({'origin': url, 'path': file_name})
    return file_name


if __name__ == '__main__':
    get_page_list()
    # parse_720_page('Ceramic720.aspx?API=MXw1NjI1fDU2MHwyNUY5RTc5NDMyM0I0NTM4ODVGNTE4MUYxQjYyNEQwQnlpdGlhbjU2MA==&DID'
    #                '=348')