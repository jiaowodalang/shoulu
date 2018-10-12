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

url=['https://www.google.com.hk/search?q=inurl:login.php', 'http://www.baidu.com/s?wd=inurl:admin.php']
proxies = {"https": "http://127.0.0.1:1080", }   
#r=requests.get(url, timeout=10, proxies=proxies)


result=[]
result2=[]

headers = {    #发送HTTP请求时的HEAD信息，用于伪装为浏览器
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

	
	
r=requests.get(url[0], timeout=10, headers=headers, proxies=proxies)
r.encoding='utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
urls=soup.find_all('a', href=True, onmousedown=True)




for k in urls:

	if 'http' in k['href'] and k['href'][0]!='/' and 'webcache.goo' not in k['href'] and 'support.goo' not in k['href']:
		result.append(k['href'])
	else:
		pass
result=set(result)

print
for i in result:
	print i
	
	
	

	
def connecturl(url):
	r=requests.get(url,allow_redirects = False,headers=headers)
	if r.status_code == 302:
		try:
			return r.headers   #返回指向的地址
		except:
			pass
			return 0
	
	
	
	
r2=requests.get(url[1], timeout=10, headers=headers)
r2.encoding='utf-8'
soup = BeautifulSoup(r2.text, 'html.parser')
urls2=soup.find_all('a', href=True)




for k in urls2:

	if 'http' in k['href'] and k['href'][0]!='/' and '?url' in k['href']:
		result2.append(k['href'])
	else:
		pass
result2=list(set(result2))
for i in range(len(result2)):
	a=connecturl(result2[i])
	print a['Location']