# 搜狐财经 https://business.sohu.com/
import json
import logging
import threading
import re

import requests
from fake_useragent import UserAgent
from lxml import etree

from spider_scripts.common_spider import Spider
from utils.multi_threads import MultiThreads

log = logging.getLogger('business_sohu')
class BusinessSohu:
    def __init__(self):
        self.url = 'https://business.sohu.com'
        self.stock_url = 'https://www.sohu.com/xchannel/tag?key=%E8%B4%A2%E7%BB%8F-%E8%82%A1%E7%A5%A8'
        self.comm_spider = Spider().get_comm_spider()
        self.thread_pool = MultiThreads().get_instance()

    def run(self):
        self.html = self.comm_spider.get_etree_page(self.url)

        # 首页内容
        # news_list = self.top_news()
        # log.info(news_list)

        # 财经-股票
        self.stock_sohu()


        # TODO 将消息写入kafka
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


    # 股票板块 https://www.sohu.com/xchannel/tag?key=%E8%B4%A2%E7%BB%8F-%E8%82%A1%E7%A5%A8
    def stock_sohu(self):
        # return 'https://www.sohu.com/xchannel/tag?key=%E8%B4%A2%E7%BB%8F-%E8%82%A1%E7%A5%A8'
        html = self.comm_spider.get_page(self.stock_url, 'text')
        # print(html)
        self.request_for_data(html)


        return
        news_list = html.xpath('//div[@class="tpl-text-feed-item"]')
        print(news_list)
        del_news_lit = []
        for news in news_list:
            del_news_lit.append({
                'title': news.xpath('./div/div/text()')[0].strip(),
                'url': news.xpath('./@href')[0],
                'content': ''
            })
        print(del_news_lit)


    def request_for_data(self, html):
        pvId = re.compile('"pvId":"\d{13}_.{7}').search(html).group()[8:]
        suv = re.compile('"suv":"[a-zA-Z0-9]+').search(html).group()[7:]
        body = {
            "clientType": 3,
            "suv": suv,
            "pvId": pvId,
            "resourceParam": [
                {
                    "context": {
                        "feedType": "XTOPIC_SYNTHETICAL",
                        "pro": "0,1"
                    },
                    "expParam": {
                    },
                    "page": 1,
                    "productParam": {
                        "categoryId": 15,
                        "mediaId": 1,
                        "productId": 1357,
                        "productType": 13
                    },
                    "requestId": "1680939500509_22091921454_xbw",
                    "resProductParam": {
                        "adTags": "20000101",
                        "productId": 1356,
                        "productType": 13
                    },
                    "resourceId": "1001563447688888320",
                    "size": 20,
                    "spm": "smpc.channel_114.block3_77_O0F7zf_1_fd"
                }
            ],
        }
        t_url = 'https://cis.sohu.com/cisv3/feeds'
        header = {
            'User-Agent': UserAgent().ie,
            'Content-Type': 'application/json;charset=utf-8'
        }
        data_list = []
        idx = 0
        while True:
            body['resourceParam'][0]['page'] = idx
            resp = requests.post(url=t_url, headers=header, data=json.dumps(body)).json()
            rd = {}
            for key in resp.keys():
                rd = resp[key]
            print(rd)
            if rd == {} or rd['data'] == []:
                break
            thread_lock = threading.Lock() # 线程间同步锁
            for item_d in rd['data']:
                self.thread_pool.submit(self.add_item_into_list, thread_lock, data_list, item_d)
                # data_list.append(self.create_item(item_d))
            idx += 1
        print("当前写入数据量" + str(len(data_list)))

    def add_item_into_list(self, thread_lock, item_list, item_d):
        item = self.create_item(item_d)
        thread_lock.acquire()
        item_list.append(item)
        print("写入数据: " + str(item))
        thread_lock.release()

    def create_item(self, item):
        ret_item = {}
        # 不同类型的数据结构不同
        if item['resourceType'] == 3:
            ret_item = {
                'title': item['backupContent']['resourceData']['contentData']['title'],
                'url': 'https://www.sohu.com/' + item['backupContent']['resourceData']['contentData']['url'],
                'content': ''
            }
        elif item['resourceType'] == 1:
            ret_item = {
                'title': item['resourceData']['contentData']['title'],
                'url': 'https://www.sohu.com' + item['resourceData']['contentData']['url'],
                'content': ''
            }
        # 填充content内容
        ret_item['content'] = self.article_detail(ret_item['url'])
        return ret_item


