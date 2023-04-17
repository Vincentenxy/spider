# 爬取同花顺页面数据
import json
import logging
import re
import string
import time

from lxml import etree
import requests
from fake_useragent import UserAgent

from mq.mq_kafka import MqKafka
import infos.url_list as urls

log = logging.getLogger('common_spider')

# 公共爬虫类
# TODO 增加动态页面爬虫
class Spider:

    comm_spider = None

    # 构造方法
    def __init__(self):
        self.kafka_client = MqKafka()

    # 返回实例
    def get_comm_spider(self):
        if Spider.comm_spider is None:
            Spider.comm_spider = Spider()
        return Spider.comm_spider

    # 生成请求头
    def get_headers(self):
        return {
            'User-Agent': UserAgent().ie
        }

    # 获取页面内容
    def get_page(self, url, code_type):
        # url格式校验
        if re.match(r'^https?:/{2}\w.+$', url) == None:
            log.error("不符合标准:"+ url)
            return None
        # 中文乱码问题
        # 1、使用content代替text获取内容，解决中文乱码问题
        t_url = self.url if url is None else url
        html = ''
        try:
            if code_type == 'text':
                html = requests.get(url=t_url, headers=self.get_headers()).text
            else:
                html = requests.get(url=t_url, headers=self.get_headers()).content
        except Exception as e:
            print('发生异常:', e)
            return ''
        return html

    # 返回处理过偶的数据
    def get_etree_page(self, url):
        ret_html = self.get_page(url, '')
        return etree.HTML(ret_html)

    # 将消息内容发送到kafka
    def send_to_kafka(self, topic, content):
        if content == "":
            log.error("数据为空错误")
            return
        print("发送数据到kafka" + str(content))
        self.kafka_client.send_msg(topic=topic, content=content)

    def find_url_key(self, url):
        l_point = url.find('.')
        if l_point == -1:
            return ''
        r_point = url.find('.', l_point+1)
        return url[url.find('//')+2: r_point]

    # 获取a标签的名称和href链接
    def get_a_info(self, html, xpath_str):
        content_ret_list = []
        a_list = html.xpath(xpath_str)
        for item_a in a_list:
            content_ret_list.append({
                'title': item_a.xpath('./text()')[0].strip(),
                'url': item_a.xpath('./@href')[0]
            })
        return content_ret_list

    # 获取文章格式
    def get_article_item(self, title, url, content):
        return {
            'title': title,
            'url': url,
            'create_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'content': content
        }