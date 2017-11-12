import os.path
from EopCrawler import EopCrawler
import shutil

if __name__ == '__main__':
    # 爬虫的工作模式：0：全站扫描覆盖已有；1：全站扫描跳过已有；2：按id降序排序依次爬取直至遇到一个曾经爬过的项目
    workMode = 1
    # 乐谱保存的路径
    path = "D:\Piano"
    # 开始页
    start = 1
    # 结束页
    end = 859

    ec = EopCrawler()
    for i in range(start, end + 1):
        html = ec.getHtml(ec.UrlPage + str(i))
        if html is not None:
            print("loaded  =>" + ec.UrlPage + str(i))
            # print(html)
            items = ec.getPageItems(html)
            j = 1
            for item in items:
                print(str(ji) + ":" + str(j) + " / " + str(len(items)))
                j += 1
                # 先简单地通过文件夹名来判断是否已经下载过
                savePath = item.getSavePath(path)

                if os.path.exists(savePath) is True:
                    if workMode == 1:
                        # 文件夹已经存在，说明已下载过，跳过
                        continue
                    elif workMode == 2:
                        # 文件夹已经存在，说明已下载过，结束程序
                        break
                    else:
                        # 文件夹已经存在，删除原有，重新下载
                        shutil.rmtree(savePath)
                item = ec.getImgUrls(item)
                ec.doDownLoadImgs(item, path)
