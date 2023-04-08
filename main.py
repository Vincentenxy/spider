# This is a sample Python script.
import logging

from spider_scripts.business_sohu import BusinessSohu
from spider_scripts.common_spider import Spider
from spider_scripts.tonghuashun import TongHuaShun


log = logging.getLogger('main')

def run():
    # 开始加载
    log.info("===========================开始执行爬虫=================================")

    # 同花顺
    ths = TongHuaShun()
    # ths.run()
    log.info("===========================同花顺已经执行完成=================================")

    # 搜狐财经
    sohu = BusinessSohu()
    sohu.run()
    log.info("===========================搜狐新闻已经执行完成=================================")


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
