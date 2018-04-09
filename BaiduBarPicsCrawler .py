#!/usr/bin/python
# coding:utf-8
# 实现一个简单的爬虫，爬取贴吧/图库图片
###################################################

import requests
import re

#####################################################################
# 根据url获取网页html内容
#####################################################################
def getHtmlContent(url):
    page = requests.get(url)		#页面get请求，获得网页对象
    return page.text		#返回网页源码

#####################################################################
#从html中解析出页数以及每页链接，以备后面一页页爬图
#正则表达式同下面图片URL解析
#####################################################################
def getPages(html,pages):
    #<a href="/p/2256306796?pn=2">下一页</a> <a href="/p/2256306796?pn=10">下一页</a>
    print('.')
    pageReg = re.compile(r'<a href="(/p/.+?pn=.+?)">下一页</a>')	#下一页链接关键字的正则表达式
    list1 = re.findall(pageReg,html)		#匹配出下一页链接
    if len(list1)!=0:
        pages.append(list1[0])		#当前页有下一页则将链接关键字存入pages list
        url = 'https://tieba.baidu.com/'+ list1[0]		#用下一页关键字拼接出下一页链接
        html = getHtmlContent(url)		#爬取下一页源码
        getPages(html, pages)		#以下一列源码递归爬取下一页链接关键字，直至最后一页
    return pages 		#返回所有页面的链接关键字List

#####################################################################
# 从html中解析出所有jpg图片的url
# 百度贴吧html中jpg图片的url格式为：<img ... src="XXX.jpg" width=...>
#####################################################################
def getJPGs(html):
    # 解析jpg图片url的正则
    jpgReg = re.compile(r'<img.+?/sign=.+?/(.+?\.jpg)" width') 		#网页中图片链接的关键字正则表达式
    jpgs = re.findall(jpgReg, html)		#正则匹配页面中所有图片链接的关键字
    return jpgs 		#返回图片关键字list

#####################################################################
# 用图片url下载图片并保存成指定文件名
#####################################################################
def downloadJPG(imgUrl,fileName):
    # 可自动关闭请求和响应的模块
    from contextlib import closing
    with closing(requests.get(imgUrl,stream = True)) as resp: 	#下载图片
        with open(fileName,'wb') as f:
            for chunk in resp.iter_content(128):
                f.write(chunk)	#下载写入图片

#####################################################################
# 批量下载图片，默认保存到当前目录下
#####################################################################
def batchDownloadJPGs(imgUrls,pp,path = './img/'):
    # 用于给图片命名
    count = 1
    num = pp*100 + count  #图片所在页数的计数器
    for url in imgUrls:
        url='http://imgsrc.baidu.com/forum/pic/item/'+url   #图片下载链接关键字转化为完整链接
        downloadJPG(url,''.join([path, '{0}.jpg'.format(num)])) 	#下载图片到指定文件夹
        print('下载完成第{0}张图片'.format(count))
        count = count + 1
        num +=1

#####################################################################
# 封装：从百度贴吧网页下载图片
#####################################################################
def download(url,pp):
    html = getHtmlContent(url)		#获取url网页源码
    jpgs = getJPGs(html) 		#获取当前网页所有图片下载链接关键字
    batchDownloadJPGs(jpgs, pp,'./img/')		#用图片关键字list下载当前页所有图片

#####################################################################
#从当前页递归获取所有下一页网页链接直至最后一页
#####################################################################
def PageOrder(html):
    print('正在爬取数据，请耐心等待_(:зゝ∠)_')
    html = getHtmlContent(html)		#获取html链接页面的源码text
    pages = ['/p/2256306796?pn=1', ]	#建立所有分页面链接关键字的list，存第一页关键字
    getPages(html, pages)		#从第一页开始递归爬取所有页（下一页）关键字
    cnt = 1		#计页数
    for url in pages:
        print('正在下载第%d页图片:'%cnt)
        url = 'https://tieba.baidu.com/'+ url 		#将关键字拼接成网页链接
        download(url,cnt)		#爬取此页所有图片链接，转换为原图链接，并下载
        cnt+=1

#####################################################################
#开始爬取某帖子所有页面所有图片
#####################################################################
def main():
    url = 'https://tieba.baidu.com/p/2256306796?pn=1'		#帖子首页链接
    PageOrder(url)		#按页爬图

if __name__ == '__main__':
    main()