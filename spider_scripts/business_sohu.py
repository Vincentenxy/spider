# 搜狐财经 https://business.sohu.com/
import logging

import requests
from lxml import etree


from spider_scripts.common_spider import Spider

log = logging.getLogger('business_sohu')
class BusinessSohu(object):
    def __init__(self):
        self.url = 'https://business.sohu.com'
        self.comm_spider = Spider().get_comm_spider()

    def run(self):
        self.html = self.comm_spider.get_etree_page(self.url)
        news_list = self.top_news()
        log.info(news_list)
        log.info("===========================搜狐新闻全部梳理完成=================================")

    def get_a_info(self, item_a):
        return {
            'title': item_a.xpath('./div/div/text()'),
            'url': item_a.xpath('./@href')
        }

    # 获取文章详情
    def article_detail(self, url):
        article_html = self.comm_spider.get_page(url=url, code_type='text')
        article_etree_html = etree.HTML(article_html)
        if article_etree_html == None: # 没有获取到相关数据直接返回
            return ''
        article_list = article_etree_html.xpath('//article[@class="article"]/p/text()')
        article_content = ''
        for article in article_list:
            article_content += article
        return article_content

    def top_news(self):
        news_list = self.html.xpath('//div[@class="FeedDataContainer"]/div/a')
        news_item_list = []
        try:
            for news in news_list:
                t_url = news.xpath('./@href')[0]
                if t_url.__contains__('track.sohu.com/promotion'): # 还需要处理，
                    print("跳过url:" + t_url)
                    continue
                n_item = {
                    'title': news.xpath('./div/div[@class="text-info"]/text()')[0].strip(),
                    'url': self.url + t_url,
                    'content': self.article_detail(self.url + t_url)
                }
                news_item_list.append(n_item)
        except Exception as e:
            print("发生异常:{}", e)

        return news_item_list


    # 股票板块
    def stock_sohu(self):
        return 'https://www.sohu.com/xchannel/tag?key=%E8%B4%A2%E7%BB%8F-%E8%82%A1%E7%A5%A8'

