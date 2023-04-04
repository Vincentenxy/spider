# 爬取同花顺页面数据
import json
import logging

from lxml import etree
import requests
from fake_useragent import UserAgent

from mq.mq_kafka import MqKafka
import infos.url_list as urls
from spider_scripts.tonghuashun import TongHuaShun


log = logging.getLogger('common_spider')
# 公共爬虫类
class Spider(object):
    def __init__(self):
        self.kafka_client = MqKafka()
        self.kafka_client.create_producer()

    # 生成请求头
    def get_headers(self):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.ie
        }
        return headers

    # 获取页面内容
    def get_page(self, url):
        # 中文乱码问题
        # 1、使用content代替text获取内容，解决中文乱码问题
        t_url = self.url if url is None else url
        html = requests.get(url=t_url, headers=self.get_headers()).content
        # 2、可以手动至指定相应的编码格式,解决乱码问题
        #html.encoding = html.apparent_encoding

        return etree.HTML(html)

    # 将消息内容发送到kafka
    def send_to_kafka(self, topic, content):
        self.kafka_client.send_msg(topic=topic, content=content)

    def run(self):
        log.info("爬虫开始执行》》》》》》")
        # for url in urls:

        ths = TongHuaShun()
        ths.url = 'https://www.10jqka.com.cn'
        ths.run()

