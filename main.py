import urllib.request
import http.cookiejar
import urllib.parse
import re
import os.path
import getpass
import gzip
from EopCrawler import EopCrawler


if __name__ == '__main__':
    ec = EopCrawler()
    # 开始页
    start = 1
    # 结束页
    end = 1
    for i in range(start, end + 1):
        html = ec.getHtml(ec.UrlPage + str(i))
        if html is not None:
            print("loaded  =>" + ec.UrlPage + str(i))
            # print(html)
            items = ec.getPageItems(html)
            j = 1
            for item in items:
                print(str(j) + " / " + str(len(items)))
                # TODO：从数据库读取是否已经爬过该项
                item = ec.getImgUrls(item)
                ec.doDownLoadImgs(item, "D:\music")
