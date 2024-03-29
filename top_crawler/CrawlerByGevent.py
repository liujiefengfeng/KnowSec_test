# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os
import sys
import time
import lxml
import gevent
import signal
import logging
import requests
import Queue
import argparse
import lxml.html as html
from log import log_service
from gevent import monkey

URL = 'http://www.topit.me/'
header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"}
last_path = '/html/body/div[@id="wrapper"]/div[@id="wrapper-inner"]/div[@id="mainbox"]/div[@id="canvasbox"]/div[@id="content"]/a[@id="item-tip"]'
first_path = '/html/body/div[@id="wrapper"]/div[@id="wrapper-inner"]/div[@id="canvas"]/div[@id="content"]/div[@class="catalog"]'
second_path = 'div[@class="e m"]/a'

logger = log_service("craw_log.log", debug=True)
gevent.monkey.patch_socket()
Pid = os.getpid()
Page_Num = 100
Num = 0
Picture_Num = 0
Path = ''
download_Num = 0
queue = Queue.LifoQueue() 

def get_url_content(url): #获取每个URL的内容
    try:
        r = requests.get(url, headers = header)
        content = r.content
        logger.info('get content of url %s:' ,url )
    except Exception ,diag:
        logger.warning('Failed requests url : %s ,reason : %s ',url,diag)
        content = None
    return content

def write_content(args): # 写入图片之前的判断
    global PicNum
    url,content = args[0],args[1]
    if PicNum == -1:
        write_now(url,content)
    elif PicNum == 0:
        logger.info('Limit picture is crawler' )
        os.kill(Pid,signal.SIGTERM)
    elif PicNum > 0:
        PicNum -= 1
        write_now(url,content)

def write_now(url,content): # 写入图片
    global download_Num
    path = url.split("/")[-1]
    try:
        f = open(os.path.join(Path,path ), 'wb+')
        f.write( content )
        logger.info('Spidered %d pictures success',download_Num )
        download_Num +=1
    except Exception , diag:
        logger.warning('Failed spider page : %s ,reason : %s ',url,diag)
        pass
    finally:
        f.close()
        
def download_image(url):   #下载图片
    content = get_url_content(url)
    if content :
        args = (url,content)
        queue.put((write_content,args))

def parse_image_url_content(content): #解析单个图片链接
    doc = html.document_fromstring( content )
    try:
        title = doc.xpath( last_path )
        links_with_label = title[0]
        image_url = links_with_label.get('href')
    except Exception,diag:
        logger.warning('Failed beacuse of ',diag)
        image_url = []
    except ValueError,diag:
        logger.warning('Failed beacuse of ',diag)
        image_url = []
    if len(image_url)>0:
        queue.put((download_image,(image_url)))
    else:
        pass

def parse_url_content(content): # 解析批量图片链接
    try:
        doc = html.document_fromstring( content )
        catalogs = doc.xpath( first_path )
        url_links = catalogs[0].findall( second_path )
    except Exception,diag:
        logger.warning('Failed beacuse of ',diag)
        url_links = []
    except ValueError,diag:
        logger.warning('Failed beacuse of ',diag)
        url_links = []
    more_urls = [i.get("href") for i in url_links]
    if len(more_urls)>0:
        for url in more_urls:
            parse_image_url(url)
    else:
        pass
        
def parse_image_url(url):  #解析单个图片链接
    content = get_url_content(url)
    queue.put((parse_image_url_content,(content)))

def parse_url(url): #解析初始链接
    logger.info('Parse the URL : %s ',url )
    content = get_url_content(url)
    queue.put((parse_url_content,(content)))

def defaultpath():  #默认路径
    nowpath = os.path.abspath('.')
    save_path = nowpath + os.sep + 'pics'
    return save_path

def cmd_line():  #命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("-n",action='store',dest = "num",help=" the number of threading,default 10",type = int,
                        default = 10
                )
    parser.add_argument("-o",action='store',dest="onwhere",help = "the place to save picture ",
                        default = defaultpath()
                )
    parser.add_argument("-l",action='store',dest="limit",type = int,help = "the limit of picture number,default limitless",
                        default = -1
                )
    results = parser.parse_args()
    return results

def Path_make(): #图片保存目录
    global Path
    if os.path.exists(Path):
        Path = Path
    else:
        os.makedirs(Path)
    
def construct_root_url ( num = 2): #网页数量
    url_prefix = URL
    url = lambda n: url_prefix + "?p=" + str(n)
    q = map(url, range(num))
    return q

def worker():  #协程控制
    Num = 2
    while Num > 0:
        if queue.empty():
            gevent.sleep(10)
            Num -= 1
            continue   
        func,args = queue.get()
        func(args)
        Num = 2
    logger.info('queue is empty,crawler over' )
    os.kill(Pid,signal.SIGTERM)

def main():  
    global Path
    global Num
    global PicNum
    global queue
    results = cmd_line()
    Num = results.num
    PicNum = results.limit
    Path = results.onwhere
    Path_make()

    urls = construct_root_url (100)
    for i in urls:
        queue.put((parse_url,i))     
    workers = []
    signal.signal(signal.SIGTERM,write_content)
    signal.signal(signal.SIGTERM,worker)
    
    for i in range( Num ):
        item = gevent.spawn(worker,)
        workers.append( item )

    gevent.joinall( workers )
    
if __name__ == '__main__':
    main()
