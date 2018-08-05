#爬虫总调度程序
import url_manager, html_downloader, html_parser, html_outputer

class SpiderMain(object):
    def __init__(self):
        #url管理器
        self.urls = url_manager.UrlManager()
        #url下载器
        self.downloader = html_downloader.HtmlDownloader()
        #url解析器
        self.parser = html_parser.HtmlParser()
        #url输出器
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("craw %d : %s" %(count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.paser(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count == 10:
                    break
                count = count + 1
            except:
                print('craw failed')
        self.outputer.output_mysql()


if __name__ == '__main__':
    #爬虫入口:百度百科的高铁词条
    root_url = "https://baike.baidu.com/item/%E9%AB%98%E9%93%81"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)