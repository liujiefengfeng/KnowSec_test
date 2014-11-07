# -*- coding:utf-8 -*-
#!/usr/bin/env python


from myThread import MyThread
import requests
import lxml
import lxml.html as html
import Queue
import sys
import os
import argparse


header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"}
last_path = '/html/body/div[@id="wrapper"]/div[@id="wrapper-inner"]/div[@id="mainbox"]/div[@id="canvasbox"]/div[@id="content"]/a[@id="item-tip"]'
first_path = '/html/body/div[@id="wrapper"]/div[@id="wrapper-inner"]/div[@id="canvas"]/div[@id="content"]/div[@class="catalog"]'
second_path = 'div[@class="e m"]/a'


def get_url_content(url):
    print 'get_url_content begin'
    r = requests.get(url, headers = header)
    return r.content

def write_content(url,content):
    path = url.split("/")[-1]
    f = open(Path+ os.sep +path , 'wb+')
    f.write( content )
    f.close()
    
def download_image(url):
    content = get_url_content(url)
    write_content(url,content)

def parse_image_url_content(content,url):
    doc = html.document_fromstring( content )
    title = doc.xpath( last_path )
    links_with_label = title[0]
    image_url = links_with_label.get('href')
    download_image(image_url)

def parse_url_content(content,url):
    print 'parse_url_content begin'
    doc = html.document_fromstring( content )
    catalogs = doc.xpath( first_path )
    url_links = catalogs[0].findall( second_path )
    more_urls = [i.get("href") for i in url_links]
    for url in more_urls:
        parse_image_url(url)
        
def parse_image_url(url):
    content = get_url_content(url)
    parse_image_url_content(content,url)

def parse_url(url):
    print 'parse_url begin '
    content = get_url_content(url)
    parse_url_content(content,url)

def defaultpath():
    nowpath = os.path.abspath('.')
    save_path = nowpath + os.sep + 'pics'
    return save_path

def cmd_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n",action='store',dest = "num",help=" the number of threading",type = int,
                        default = 10
                )
    parser.add_argument("-o",action='store',dest="onwhere",help = "the place to save picture ",
                        default = defaultpath()
                )
    parser.add_argument("-l",action='store',dest="limit",type = int,help = "the limit of picture number",
                        default = -1
                )
    results = parser.parse_args()
    return results

def Path_make(Path):
    if os.path.exists(Path):
        return Path
    else:
        os.makedirs(Path)
        return Path
    
def construct_root_url ( num = 2):
    url_prefix = 'http://www.topit.me/'
    url = lambda n: url_prefix + "?p=" + str(n)
    q = map(url, range(num))
    return q
    #queue = set(q)
    #return queue

def begin(queue):
    while queue.qsize >0:
        url = queue.get()
        parse_url(url)

    
def main():
    #url = 'http://i10.topit.me/l096/10096776104754124b.jpg'
    #download_image(url)
    #url = 'http://www.topit.me/item/4879559'
    #url = 'http://www.topit.me/'
    #print url
    results = cmd_line()
    Num = results.num
    global Path
    Path = results.onwhere
    Path = Path_make(Path)
    global PicNum
    PicNum = results.limit
    #parse_url(url)
    urls = construct_root_url (5)
    queue = Queue.Queue()
    for url  in urls:
        queue.put(url)
        
    threads = []
    for i in range(Num):
        t = MyThread(begin,(queue,),begin.__name__)
        threads.append(t)

    for i in range(Num):
        threads[i].start()

    for i in range(Num):
        threads[i].join()

    print 'all DONE'

if __name__ == '__main__':
    main()
