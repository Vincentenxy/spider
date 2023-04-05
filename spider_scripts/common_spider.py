# 爬取同花顺页面数据
import json
import logging

from lxml import etree
import requests
from fake_useragent import UserAgent

from mq.mq_kafka import MqKafka
import infos.url_list as urls

log = logging.getLogger('common_spider')

# 公共爬虫类
# TODO 增加动态页面爬虫
class Spider(object):

    comm_spider = None;

    # 构造方法
    def __init__(self):
        self.kafka_client = MqKafka()
        self.kafka_client.create_producer()

    # 返回实例
    def get_comm_spider(self):
        if self.comm_spider is None:
            self.comm_spider = Spider()
        return self.comm_spider

    # 生成请求头
    def get_headers(self):
        return {
            'User-Agent': UserAgent().ie
        }

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
    def send_to_kafka(self, *topic, content):
        if content == "":
            return
        self.kafka_client.send_msg(topic='', content=content)

    def find_url_key(self, url):
        l_point = url.find('.')
        if l_point == -1:
            return ''
        r_point = url.find('.', l_point+1)
        return url[url.find('//')+2: r_point]