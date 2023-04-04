# 爬取同花顺页面数据
import json
from lxml import etree
import requests
from fake_useragent import UserAgent

from mq.mq_kafka import MqKafka


class TongHuaShun(object):
    def __init__(self):
        self.url = 'https://www.10jqka.com.cn'
        self.kafka_client = MqKafka()
        self.kafka_client.create_producer()

    def get_headers(self):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.ie
        }
        return headers

    def get_page(self, url):

        # 中文乱码问题
        # 1、使用content代替text获取内容，解决中文乱码问题
        t_url = self.url if url is None else url
        print(t_url)
        html = requests.get(url=t_url, headers=self.get_headers()).content
        # 2、可以手动至指定相应的编码格式,解决乱码问题
        #html.encoding = html.apparent_encoding

        return etree.HTML(html)

    def parse_page(self, html):
        # content_list = html.xpath('//ul[@class="content newhe"]/li/a/text()')
        ori_item_list = html.xpath('//ul[@class="content newhe"]')
        del_item_list = []
        for item in ori_item_list:
            obj = {}
            a_list = item.xpath('.//li/a')
            for a in a_list:
                obj['name'] = a.xpath('.//text()')
                obj['href'] = a.xpath('.//@href')[0].strip()
                self.parse_detail_page(obj['href'])


    def parse_detail_page(self, url):
        if url is None:
            print("url is blank!")
            return
        content_html = self.get_page(url)
        content = ''
        content_strs= content_html.xpath(self.xpath_cre(url))
        for cont in content_strs:
            content += cont
        self.kafka_client.send_msg('test', content)


    # 获取xpath表达式
    def xpath_cre(self, url):
        # 1、同花顺官方网站文章
        if url.__contains__('10jqka.com'):
            return  '//div[@class="main-text atc-content"]/p/text()'

        # 2、微信小程序的文章
        if url.__contains__('weixin.qq'):
            # class ="js_darkmode__1"
            return '//span[@class="js_darkmode__0"]'

        return ''

    def run(self):
        page_html = self.get_page(None)
        self.parse_page(page_html)



    # https: // github.com / ymcui / Chinese - BERT - wwm