from spider_scripts.common_spider import Spider  # 金融界 http://www.jrj.com.cn/


class JinRongJie(object):

    xpath_list = []

    def __init__(self):
        self.url = 'http://www.jrj.com.cn/'
        self.comm_spider = Spider().get_comm_spider()

    def run(self):
        self.html = self.comm_spider.get_page(self.url)
        # 对数据进行处理
        self.top_news()

    # 热点数据
    def top_news(self):
        news_list = self.html.xpath('//div[@class="test-s1"]/p')

        print(news_list)

        # nn_list = []
        # for news in news_list:
        #     nn_list.append(news.xpath('./a/text()'))
        #
        # print(nn_list)

        # a_info_list = self.comm_spider.get_a_info()


jrj = JinRongJie()
jrj.run()