# This is a sample Python script.
import logging

from spider_scripts.common_spider import Spider

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    spider = Spider()
    spider.run()

# nlp地址
# https: // github.com / ymcui / Chinese - BERT - wwm