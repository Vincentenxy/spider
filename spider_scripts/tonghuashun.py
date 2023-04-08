# 爬取同花顺页面数据
import logging

from spider_scripts.common_spider import Spider


class TongHuaShun:

    xpath_list = {
        't.10jqka': '//div[@class="wdwrap post-text-main c444 ql-editor"]/p/text() | //div[@class="wdwrap post-text-main c444 ql-editor"]/p/*/text()',
        'stock.10jqka': '//div[@class="main-text atc-content"]/p/text()',
        'news.10jqka': '//div[@class="main-text atc-content"/p/text()',
        'weixin.qq': '//span[@class="js_darkmode__0"]'
    }

    def __init__(self):
        self.url = 'https://www.10jqka.com.cn'
        self.comm_spider = Spider().get_comm_spider()
    def run(self):
        page_html = self.comm_spider.get_page('https://www.10jqka.com.cn')
        # self.top_news(page_html)
        self.economy_news(page_html)
        self.industry_news()

    # 获取文章详情
    def parse_detail_page(self, url):
        if url is None:
            print("url is blank!")
            return
        content_html = self.comm_spider.get_page(url)
        content = ''
        try:
            content_strs = content_html.xpath(TongHuaShun.xpath_list[self.comm_spider.find_url_key(url)])
        except Exception as e:
            logging.error(e)
            return ''
        for cont in content_strs:
            content += cont
        return content

    # 得到a标签内容
    def get_a_info(self, html, xpath_str):
        content_ret_list = []
        a_list = html.xpath(xpath_str)
        for item_a in a_list:
            content_ret_list.append({
                'title': item_a.xpath('./text()')[0].strip(),
                'url': item_a.xpath('./@href')[0]
            })
        return content_ret_list



    # 主要新闻
    def top_news(self, html):
        news_list = html.xpath('//div[@class="fr tt_word yah"]/p/a/@href')
        for news in news_list:
            article_content = self.parse_detail_page(news).strip()
            print(news + " 文章内容:\n" + article_content)
            # self.comm_spider.send_to_kafka(content=article_content)

    # 投资机会
    def invest_chance(self):
        return 'class="tab sub-box rec-login"'

    # 财经要文
    def economy_news(self, html):
        a_info_list = self.get_a_info(html, '//ul[@tpe-plugin="preview_wap_row"]/li/a')
        for item_a in a_info_list:
            item_a['content'] = self.parse_detail_page(item_a['url'])
            print(item_a)

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

