# 搜狐财经 https://business.sohu.com/
from spider_scripts.common_spider import Spider

class BusinessSohu(object):
    def __init__(self):
        self.url = 'https://business.sohu.com'
        self.comm_spider = Spider().get_comm_spider()

    def run(self):
        self.html = self.comm_spider.get_page(self.url)
        self.top_news()

    def get_a_info(self, item_a):
        return {
            'title': item_a.xpath('./div/div/text()'),
            'url': item_a.xpath('./@href')
        }

    def top_news(self):
        news_list = self.html.xpath('//div[@class="FeedDataContainer"]/div/a')
        news_item_list = []
        for news in news_list:
            news_item_list.append({
                'title': news.xpath('./div/div[@class="text-info"]/text()')[0].strip(),
                'url': self.url + news.xpath('./@href')[0]
            })
        print(news_item_list)


bsh = BusinessSohu()
bsh.run()