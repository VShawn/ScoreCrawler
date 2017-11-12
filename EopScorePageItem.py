import os.path


# 一篇谱子的抽象类
class EopPageItem(object):
    def __init__(self, strid,url, date,title,author):
        self.strid = str(strid)
        self.id = int(strid)
        self.url = str(url)
        self.date = str(date)
        self.title = str(title)
        self.author = str(author)
        # 五线谱地址
        self.staveUrl = 'http://www.everyonepiano.cn/Stave-'+str(self.id)+'.html'
        self.staveImgs = []
        # 简谱地址
        self.numberUrl = 'http://www.everyonepiano.cn/Number-'+str(self.id)+'.html'
        self.numberImgs = []

    def print_attrs(self):
        print(
            'id:', self.id, ',',
            'url:', self.url, ',',
            'date:', self.date, ',',
            'title:', self.title, ',',
            'author:', self.author, ',',
        )
    # 获取存储路径
    def getSavePath(self, parentdir):
        # 文件夹取个长名字，免得重复了
        return os.path.join(parentdir, self.title + "_" + self.author + "_" + self.strid)
