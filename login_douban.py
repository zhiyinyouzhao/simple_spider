#!/usr/bin/python2.6
# -*- coding:utf-8 -*-  
# author = "Mr zh"  
# date  = "2016/7/10"  

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

#豆瓣登录页面
loginUrl = 'https://accounts.douban.com/login'
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
"form_email":"XXps@126.com",
"form_password":"XX",
"source":"index_nav",
"remember":"on"
}
#首次提交请求登录
response=opener.open(loginUrl, urllib.urlencode(params))
#返回页面信息，BeautifulSoup格式化
content = response.read()
soup = BeautifulSoup(content)
#利用find方法获取captcha_id,并将验证码图片保存在本地相同目录
captcha_imageadd = soup.find('img','captcha_image').get('src')
captcha_id = soup.find(attrs={"name": "captcha-id"}).get('value')
captcha_picture=urllib.urlretrieve(captcha_imageadd,"captcha.jpg")
#提交验证码登录，手工输入
captcha_solution = raw_input("输入验证码:\n")
params['captcha-solution'] = captcha_solution  
params['captcha-id'] = captcha_id 
response=opener.open(loginUrl, urllib.urlencode(params))
#登录成功后跳转到豆瓣主页
if response.geturl() == "https://www.douban.com/":
	print "Welcome to you!"
	print "准备来西豆发个帖子"
	#获取ck值
	for c in list(cookie):
		if c.name == 'ck':
			ck = c.value.strip('"')
	#发新帖
	addtopicurl = "https://www.douban.com/group/xiandouban/new_topic"
	post_data = urllib.urlencode({
		'ck': ck, 
		'rev_title':"西豆ers,新人来报道", 
		'rev_text': "晚上看球吗，猜猜谁冠军",
		'rev_submit':'好了，发言'
		})
	
	request = urllib2.Request(addtopicurl)  
	request.add_header("Referer", addtopicurl) 
	response = opener.open(request, post_data) 
	if response.geturl() == "https://www.douban.com/group/xiandouban/":
		print "Success!" 

