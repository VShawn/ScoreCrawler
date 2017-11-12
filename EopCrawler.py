from bs4 import BeautifulSoup
from EopScorePageItem import EopPageItem
import gzip
import urllib.request
import http.cookiejar
import urllib.parse
import os.path
import time


class EopCrawler(object):
    def __init__(self):
        return

    UrlPage = "http://www.everyonepiano.cn/Music.html?canshu=id&paixu=desc&p="
    UrlHome = "http://www.everyonepiano.cn"
    op = None

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'accounts.pixiv.net',
        'Referer': 'http://www.everyonepiano.cn/Music.html?paixu=desc',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'
    }

    def ungzip(self,data):
        try:
            data = gzip.decompress(data)
        except Exception as e:
            print(e)
        return data

    def getopener(self, header):
        cj = http.cookiejar.CookieJar()
        cp = urllib.request.HTTPCookieProcessor(cj)
        op = urllib.request.build_opener(cp)
        h = []
        for key, value in header.items():
            elem = (key, value)
            h.append(elem)
        op.addheaders = h
        return op

    def getHtml (self, url):
        if self.op is None:
            self.op = self.getopener(self.headers)
        html = None
        with self.op.open(url) as f:
            if f.status == 200:
                op_key = self.op.open(url)
                data = op_key.read()
                op_key.close()
                html = self.ungzip(data).decode()
        return html




    def getPageItems(self, html):
        rootSoup = BeautifulSoup(html, 'lxml')
        # 获得#EOPMain中的所有class=MusicIndexBox的div
        selector = rootSoup.select('div.MusicIndexBox')
        '''
                    <div class="MusicIndexBox">
                      <div class="MITitle">
                        <div class="MIMusicNO hidden-xs">0008579</div>
                        <a href="/Music-8579-别-薛之谦.html" title="别-薛之谦" target="_blank" class="Title">别-薛之谦</a>-
                        <a href="/Music.html?author=%E8%96%9B%E4%B9%8B%E8%B0%A6" style="color:green;" title="薛之谦">薛之谦</a></div>
                      <div class="row">
                        <div class="col-xs-12 col-sm-10 col-md-8 MIMusicBar" style="background:url(/Public/img2016/launch_cn.png) no-repeat bottom right;">
                          <div class="MIMusicPICDiv">
                            <a href="/Music-8579-别-薛之谦.html" title="别-薛之谦" target="_blank">
                              <img src="/pianomusic/009/0008579/0008579-small.jpg" class="MIMusicPIC" alt="别-薛之谦" onerror="this.src='/Public/img2015/noeoppic.jpg'"></a>
                            <div class="MIMusicUpdate">2017/11/11</div></div>别是由歌手薛之谦作词、作曲并演唱的一首歌曲，发行于2017年10月31日。下面是别钢琴谱，感兴趣的朋友可以使用。
                          <div class="MusicBtn1 hidden-xs">曲谱格式：&nbsp;
                            <a href="/Music-8579-别-薛之谦.html#别-薛之谦五线谱下载" title="下载：618次" target="_blank">
                              <img src="/Public/img2016/stave.png" width="36" height="21" /></a>
                            <a href="/Music-8579-别-薛之谦.html#别-薛之谦双手简谱下载" title="下载：817次" target="_blank">
                              <img src="/Public/img2016/num.png" width="36" height="21" /></a>
                            <a href="/Music-8579-别-薛之谦.html#别-薛之谦EOP文件下载" title="下载：301次" target="_blank">
                              <img src="/Public/img2016/eop.png" width="36" height="21" style="margin-right:20px;" /></a>上传者：
                            <font color="#666666">EOP小编</font></div>
                        </div>
                        <div class="hidden-xs col-sm-2 col-md-2 MIMusicInfo2">
                          <span class="MIMusicInfo2Num">2646</span>&nbsp;
                          <span class="MIMusicInfo2Time">次</span></div>
                        <div class="hidden-xs hidden-sm col-md-2 MIMusicInfo3">
                          <a href="/Mp3-8579-别-薛之谦.html" target="_blank" title="我要试听">
                            <div class="BigBtn_MP3"></div>
                          </a>
                          <a href="/Music/returns/8579" target="_blank" title="相关视频">
                            <div class="BigBtn_Video"></div>
                          </a>
                        </div>
                      </div>
                      <div class="hidden-sm hidden-md hidden-lg MISmallBtn">
                        <a href="/Music/returns/8579" target="_blank" title="相关视频">
                          <div class="MBtn_Video"></div>
                        </a>
                        <a href="/Mp3-8579-别-薛之谦.html" target="_blank" title="我要试听">
                          <div class="MBtn_Mp3"></div>
                        </a>
                        <a href="/Music-8579-别-薛之谦.html#别-薛之谦EOP文件下载" title="下载：301次" target="_blank">
                          <div class="MBtn_EOP"></div>
                        </a>
                        <a href="/Music-8579-别-薛之谦.html#别-薛之谦双手简谱下载" title="下载：817次" target="_blank">
                          <div class="MBtn_Num"></div>
                        </a>
                        <a href="/Music-8579-别-薛之谦.html#别-薛之谦五线谱下载" title="下载：618次" target="_blank">
                          <div class="MBtn_Stave"></div>
                        </a>
                      </div>
                    </div>
        '''
        # 遍历处理div
        items = []
        for child in selector:
            strid = str(child.select('div.MITitle > div')[0].string)
            author = str(child.select('div.MITitle > a')[1].string)
            title = str(child.select('div.MITitle > a')[0].string)
            title = title.replace("-" + author, '')
            url = child.select('div.MITitle > a')[0]['href']
            url = self.UrlHome + url
            date = child.select('div.MIMusicUpdate')[0].string
            items.append(EopPageItem(strid, url, date,title,author))
        return items

    # 分析出谱子图片的url
    def getImgUrls(self, item):
        # 处理五线谱页
        html = self.getHtml(item.staveUrl)
        if html is not None:
            rootSoup = BeautifulSoup(html, 'lxml')
            selector = rootSoup.select('div.PngDiv > ul > li')
            for child in selector:
                item.staveImgs.append(self.UrlHome + child.select('img')[0]['src'])
        # 处理简谱页
        html = self.getHtml(item.numberUrl)
        if html is not None:
            rootSoup = BeautifulSoup(html, 'lxml')
            selector = rootSoup.select('div.PngDiv > ul > li')
            for child in selector:
                item.numberImgs.append(self.UrlHome + child.select('img')[0]['src'])
        return item

    # 执行谱子下载
    def doDownLoadImgs(self,item, parentdir):
        # 储存路径
        path = item.getSavePath(parentdir)
        if os.path.exists(path) is False:
            os.makedirs(path)
        if self.op is None:
            self.op = self.getopener(self.headers)
        i = 1
        # 下载五线谱
        for url in item.staveImgs:
            imgPath = os.path.join(path, item.title + "_stave_" + str(i).zfill(3) + ".jpg")
            try:
                with self.op.open(url) as f:
                    if f.status == 200:
                        with open(imgPath, 'wb') as o:
                            o.write(f.read())
                            print('成功下载 -> %s' % imgPath)
                            o.close()
                            # 等待,爬得太快容易被发现
                            time.sleep(0.5)
            except Exception as e:
                with open(os.path.join(parentdir, "log.txt"), "a") as f:
                    f.write(e.args[1] + " at " + imgPath + "\r\n")
                    continue
            i += 1
        # 下载简谱
        i = 1
        # 下载五线谱
        for url in item.numberImgs:
            try:
                with self.op.open(url) as f:
                    imgPath = os.path.join(path, item.title + "_number_" + str(i).zfill(3) + ".jpg")
                    if f.status == 200:
                        with open(imgPath, 'wb') as o:
                            o.write(f.read())
                            print('成功下载 -> %s' % imgPath)
                            o.close()
                            # 等待,爬得太快容易被发现
                            time.sleep(0.5)
            except Exception as e:
                with open(os.path.join(dir, "log.txt"), "a") as f:
                    f.write(e + "\r\n")
                    continue
            i += 1
        # 保存信息
        with open(os.path.join(path, item.title + ".txt"), "w") as f:
            f.write("      Form:\t\t" + item.url + "\r\n")
            f.write("        ID:\t\t" + item.strid + "\r\n")
            f.write("UpdateDate:\t\t" + item.date + "\r\n")
            f.write("   Sorting:\t\tShawn\r\n")
        return

