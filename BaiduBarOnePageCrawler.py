#!/usr/bin/python
# coding:utf-8
# 实现一个简单的爬虫，爬取贴吧/图库图片
import requests
import re

# 根据url获取网页html内容
def getHtmlContent(url):
    page = requests.get(url)
    return page.text

# 从html中解析出所有jpg图片的url
# 百度贴吧html中jpg图片的url格式为：<img ... src="XXX.jpg" width=...>
def getJPGs(html):
    # 解析jpg图片url的正则
    jpgs = []
    print(jpgs)
    #https: // www.instagram.com / p / BgfjlvlDg4H /?taken - by = tee_jaruji
    jpgReg1 = re.compile(r'"shortcode":"(.+?)"')
    print(jpgReg1)
    jpgs1 = re.findall(jpgReg1, html)
    print(jpgs1)
    for url1 in jpgs1:
        print('https://www.instagram.com/p/'+url1+'/?taken-by=tee_jaruji')
        html = getHtmlContent('https://www.instagram.com/p/'+url1+'/?taken-by=tee_jaruji')
        #750w,https://scontent-nrt1-1.cdninstagram.com/vp/cdb59589c0f5abc42a923bf73b5506d0/5B36AA4F/t51.2885-15/e35/29415875_200094744088937_5818414838958784512_n.jpg 1080w"
        #print(html)
        jpgReg2 = re.compile(r'750.+?{"src":"(https://.+?\.jpg)","config_width":1080')
        print(jpgReg2)
        jpgs2 = re.findall(jpgReg2,html)
        print(jpgs2)
        if len(jpgs2)!=0:
            jpgs.append(jpgs2[0])
    print(jpgs)
    return jpgs

# 用图片url下载图片并保存成制定文件名
def downloadJPG(imgUrl,fileName):
    # 可自动关闭请求和响应的模块
    from contextlib import closing
    with closing(requests.get(imgUrl,stream = True)) as resp:
        with open(fileName,'wb') as f:
            for chunk in resp.iter_content(128):
                f.write(chunk)

# 批量下载图片，默认保存到当前目录下
def batchDownloadJPGs(imgUrls,path = './img/'):
    # 用于给图片命名
    count = 1
    for url in imgUrls:
        print(url)
        downloadJPG(url,''.join([path,'{0}.jpg'.format(count)]))
        print('下载完成第{0}张图片'.format(count))
        count = count + 1

# 封装：从百度贴吧网页下载图片
def download(url):
    html = getHtmlContent(url)
    #print(html)
    jpgs = getJPGs(html)
    batchDownloadJPGs(jpgs, './img/')

def main():
    url = 'https://www.instagram.com/tee_jaruji/'
    download(url)

if __name__ == '__main__':
    main()
