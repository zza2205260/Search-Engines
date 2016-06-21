# -*- coding: utf-8 -*-

import urllib2
import re
import uniout
import StringIO,gzip
import sys

sys.setrecursionlimit(1000000)

dataList = []
used_url = []
loopbool = []

# 存储有内容的网页数量
webcount = 1000
keyword = "习近平"


class webdata:
	url = ''
	count = 0
	html_context = ""
	def __init__(self, u , c , h):
		self.url = u
		self.count = c
		self.html_context = h
     
     
def gethtml(url):
	for x in used_url:
		if url == x:
			return
	used_url.append(url)
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	try:
		request = urllib2.Request(url,headers = headers)
		response = urllib2.urlopen(request)
		data = response.read()
		if 'gzip' == response.headers.get('Content-Encoding'):
			compressedstream = StringIO.StringIO(data)
			gziper = gzip.GzipFile(fileobj=compressedstream)
			data = gziper.read()		
			pass
		if len(loopbool) == 0:
			analysishtml(data)
		return data
	except Exception, e:
		print e
 
def analysishtml(htmlstr):
	pong = re.compile('"http://.+?sina.+?.shtml"')
	result = pong.findall(htmlstr)
	for x in xrange(0,len(result)):
		if len(loopbool) > 0:
			print "这里有么"
			serchto()
			break
		isset = True
		h_url = result[x].replace('"','')
		for j in xrange(0,len(dataList)):
			if dataList[j].url == h_url:
				dataList[j].count = dataList[j].count + 1
				isset = False
		if isset:
			context = gethtmlcontext(gethtml(h_url))
			if context != None:
				a_data = webdata(h_url , 0 , context)
				dataList.append(a_data)
				print ("存储有内容的网页数量%d"%(len(dataList)))
				if len(dataList) == webcount:
					isset = False
					loopbool.append('f') 

def gethtmlcontext(htmlstr):
	if htmlstr == None:
		return
	pong = re.compile('<p>([^"]+?)</p>')
	result = pong.findall(htmlstr)
	if len(result) > 0:
		context_str = ''.join(result)
		return context_str
	else:
		return
 

def serchto():
	serchend = []
	for x in dataList:
		if x.html_context.find(keyword) != -1:
			serchend.append(x)
			print x.url
	print len(serchend)


gethtml('http://www.sina.com.cn') 














