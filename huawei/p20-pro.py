import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path="phantomjs.exe")


def get_page_info():
    url = "https://sale.vmall.com/p20buy.html"
    # res = requests.get(url=url, headers={
    #     "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/65.0.3325.181 Safari/537.36 ',
    #     "Host": "sale.vmall.com",
    # })
    # if res.status_code == 200:
    #     be = BeautifulSoup(res.content.decode())
    #     choose_area = be.find("div", id="choose_area")
    #     print(choose_area.html)
    # else:
    #     print("页面获取失败，HTTP请求代码为：%s" % res.status_code)
    driver.get(url)
    driver.find_element_by_id("skuGroupTag-33023").click()

    print(driver.find_element_by_id("skuGroupTag-33031").location_once_scrolled_into_view.values())


if __name__ == "__main__":
    get_page_info()