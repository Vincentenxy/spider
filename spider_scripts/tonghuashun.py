# 爬取同花顺页面数据
import json
import logging

from lxml import etree
import requests
from fake_useragent import UserAgent

from mq.mq_kafka import MqKafka
from spider_scripts.common_spider import Spider


class TongHuaShun(object):
    def __init__(self):
        self.url = 'https://www.10jqka.com.cn'
        self.comm_spider = Spider().get_comm_spider()
    def run(self):
        page_html = self.comm_spider.get_page('https://www.10jqka.com.cn')
        self.top_news(page_html)

    # 获取xpath表达式
    def xpath_dispatch(self, url):
        # 1、同花顺官方网站文章
        if url.__contains__('10jqka.com'):
            return  '//div[@class="main-text atc-content"]/p/text()'

        # 2、微信小程序的文章
        if url.__contains__('weixin.qq'):
            # class ="js_darkmode__1"
            return '//span[@class="js_darkmode__0"]'
        return ''

    # def parse_page(self, html):
    #     # content_list = html.xpath('//ul[@class="content newhe"]/li/a/text()')
    #     ori_item_list = html.xpath('//ul[@class="content newhe"]')
    #     del_item_list = []
    #     for item in ori_item_list:
    #         obj = {}
    #         a_list = item.xpath('.//li/a')
    #         for a in a_list:
    #             obj['name'] = a.xpath('.//text()')
    #             obj['href'] = a.xpath('.//@href')[0].strip()
    #             self.parse_detail_page(obj['href'])

    # 获取文章详情
    def parse_detail_page(self, url):
        if url is None:
            print("url is blank!")
            return
        content_html = self.comm_spider.get_page(url)
        content = ''
        content_strs= content_html.xpath(self.xpath_dispatch(url))
        for cont in content_strs:
            content += cont
        print("获取内容：" + content)
        return content

    # 主要新闻
    def top_news(self, html):
        news_list = html.xpath('//div[@class="fr tt_word yah"]//p/a/@href')
        for news in news_list:
            article_content = self.parse_detail_page(news)
            self.comm_spider.send_to_kafka(content=article_content)

    # 投资机会
    def invest_chance(self):
        return 'class="tab sub-box rec-login"'

    # 财经要文
    def economy_news(self):
        return 'class="tab sub-box"'

    # 产经新闻
    def industry_news(self):
        return 'class="control ta-parent-box cpbd"'

    # 研报精选
    def research_report(self):
        return 'class="control ta-parent-box cpbd"'


    # 百家论股
    # class ="sub-box module  fl"

    # 股市学堂
    # TODO

    # 港股
    # TODO

    # 美股
    # TODO

    # 新三版
    # TODO

    # 债券
    # TODO

    # 基金要文
    # TODO

    # 热销基金
    # TODO

    # 黄金要文
    # TODO

    # 期货要文
    # TODO

    # 热门圈子
    # TODO

    # 圈子精选
    # TODO

    # 理财
    # TODO

    # 外汇
    # TODO

