#!/usr/bin/python2.6
# -*- coding:utf-8 -*-  
# author = "Mr zh"  
# date  = "2016/7/10"  

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

#西工大成绩系统
loginUrl = 'http://222.24.211.70:7001/grsadmin/servlet/studentLogin'
#头信息
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip, deflate, sdch",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Cache-Control":"max-age=0",
	"Connection":"keep-alive"
}
#声明一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#创建字典存放表单信息
params = {
"USER":"2015262607",
"PASSWORD":"2015262607",
"TYPE":"AUTH"
}
#首次提交请求登录
request = urllib2.Request(loginUrl,urllib.urlencode(params))
response=opener.open(request)
if response.geturl() == "http://222.24.211.70:7001/grsadmin/servlet/studentMain":
	print "welconme to you !"

#print response.read().decode("gb2312")
gradeUrl = "http://222.24.211.70:7001/grsadmin/servlet/studentMain"
postdata = {
		"MAIN_NEXT_ACTION":"LL",
		"MAIN_PURPOSE":"/jsp/student_JhBrow.jsp",
		"MAIN_SUB_ACTION":"ä¯ÀÀ³É¼¨",
		"MAIN_TYPE":3
		}
request = urllib2.Request(gradeUrl,urllib.urlencode(postdata))
response=opener.open(request)
content = response.read()
soup = BeautifulSoup(content)

table = soup.find(cellspacing="0",cellpadding="4",border="1",bordercolordark="#ffffff")

credit = []
rows = table.find_all("tr")
for row in rows:
	cols = row.find_all("td")
	courseCode = cols[0].get_text().strip()
	courseName = cols[1].get_text().strip()
	courseType = cols[2].get_text().strip()
	courseTerm = cols[3].get_text().strip()
	courseCredit = cols[4].get_text().strip()
	if cols[5].get_text().strip() != None:
		courseScore = cols[5].get_text().strip()
	else:
		courseScore = "none"
	if cols[6].get_text().strip() != None:
		courseDate = cols[6].get_text().strip()
	else:
		courseDate = "none"
	print "%s %s %s %s %s %s %s " % (courseCode,courseName,courseType,courseTerm,courseCredit,courseScore,courseDate)

