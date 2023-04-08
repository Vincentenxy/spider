# This is a sample Python script.
import logging

from spider_scripts.business_sohu import BusinessSohu
from spider_scripts.common_spider import Spider
from spider_scripts.tonghuashun import TongHuaShun


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def run():
    # 开始加载
    logging.info("开始执行爬虫》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》")

    # 同花顺
    ths = TongHuaShun()
    # ths.run()

    # 搜狐财经
    sohu = BusinessSohu()
    sohu.run()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()

    # url = 'http://news.10jqka.com.cn/20230406/c646179214.shtml'
    # comm_spider = Spider()
    # html = comm_spider.get_page(url)
    # content = html.xpath('//div[@class="main-text atc-content"/p/text()')
    # for cont in content:
    #     print(cont)
    #
    # print("----->")


# nlp地址
# https: // github.com / ymcui / Chinese - BERT - wwm
