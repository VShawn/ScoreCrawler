import urllib.request
import http.cookiejar
import urllib.parse
import re
import os.path
import getpass
import gzip
import EopCrawler


if __name__ == '__main__':
    ec = EopCrawler();

    i = 1;

    html = ec.getHtml(ec.UrlPage+ i)
    if html != None:
        #print(html)
        items = ec.getPageItems(html)

    i += 1
    #TODO 从数据库读取是否已经爬过该项