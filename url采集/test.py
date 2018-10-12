#!/usr/bin/env python
# coding=utf-8


'''
url采集
2018/3/27

'''



from bs4 import BeautifulSoup
from concurrent import futures
import re
import getopt
import gevent
from lxml import etree
import requests
import sys, getopt
reload(sys)
sys.setdefaultencoding('utf-8')

url=['https://www.google.com/search?q=', 'http://www.baidu.com/s?wd=']
proxies = {"https": "http://127.0.0.1:1080", }   
#r=requests.get(url, timeout=10, proxies=proxies)



#全局变量
url1 = []
zuizhongurl = []
zuizhongurl2 = []
key=""
page=10
google=False

headers = {    #发送HTTP请求时的HEAD信息，用于伪装为浏览器
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }




def usage():
	print "Usage:"
	print "      .py -k [key] -p [page]"
	sys.exit(0)

	
#提取百度302跳转location，获取目标url
def connecturl(url):
	r=requests.get(url,allow_redirects = False,headers=headers)
	if r.status_code == 302:
		try:
			return r.headers['location']    #返回指向的地址
		except:
			pass
			return False


#url提取，使用xpath，使用gevent协程并发
def baidu_geturl(url):
	result2=[]
	r=requests.get(url, timeout=10, headers=headers)
	r.encoding='utf-8'
	soup = BeautifulSoup(r.text, 'html.parser')
	urls2=soup.find_all('a', href=True)
	for k in urls2:

		if 'http' in k['href'] and k['href'][0]!='/' and '?url' in k['href']:
			result2.append(k['href'])
		else:
			pass
	result=list(set(result2))
	
	events=[gevent.spawn(connecturl,url) for url in result]
	data=gevent.joinall(events)
	p=[]
	for d in data:
		p.append(d.get())
	return p


def google_geturl(url):
	r=requests.get(url, timeout=10, headers=headers, proxies=proxies)
	r.encoding='utf-8'
	soup = BeautifulSoup(r.text, 'html.parser')
	urls=soup.find_all('a', href=True, onmousedown=True)
	result_google=[]
	for k in urls:

		if 'http' in k['href'] and k['href'][0]!='/' and '.google' not in k['href']:
			result_google.append(k['href'])
		else:
			pass
	result_google=list(set(result_google))

	return result_google

	
def main():
	global key
	global page
	global url
	global google
	f = open('url.txt','w')
	try:
		opts,args =getopt.getopt(sys.argv[1:],"hgk:p:",["help","key=","page=","google"])
	except getopt.GetoptError:
		sys.exit(0)
	if not len(sys.argv[1:]):
		usage()
	for name,value in opts:
		if name in ("-h","--help"):
			usage()
		if name in ("-k","--key"):
			key=str(value)
			if key=='':
				print "make sure you have key for search::",key
				usage()
			else:
				print "your key for search:",key
		if name in ("-p","--page"):
			page=int(value)
			print "your page select:",page
		if name in ("-g","--google"):
			google = True
	if not sys.argv[1]:
		usage()
	if google:
		print "use google search."
		
	for i in range(page):
		url1.append(i*10)
	for i in url1:
		zuizhongurl.append(url[1]+key+'&pn='+str(i))
	for i in url1:
		zuizhongurl2.append(url[0]+key+'&start='+str(i))
	
	with futures.ThreadPoolExecutor(max_workers=3) as executor:
		future = [executor.submit(baidu_geturl,url) for url in zuizhongurl]
		urls=[]
		for p in future:
			urls.append(p.result())
	with futures.ThreadPoolExecutor(max_workers=3) as executor:
		future = [executor.submit(google_geturl,url) for url in zuizhongurl2]
		for p in future:
			urls.append(p.result())
	for i in urls:
		for j in i:
			if '.baidu' not in j:
				f.write(j)
				f.write('\n')
	f.close()
		
	print "good job!! in url.txt"	
		
		
		
		
		
main()
		