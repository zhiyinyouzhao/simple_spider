#!/usr/bin/env python
#coding=utf-8
from bs4 import BeautifulSoup
import urllib
import urllib2

class QSBK(object):
	#初始化定义一些变量
	def __init__(self):
		self.pageIndex=1
		self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0)"
		self.headers = {"User-Agent":self.user_agent}
		#存放段子的列表，其中每个元素代表一页的段子
		self.one_page = []
		#存放程序是否继续运行标志
		self.enable = False
	def get_page(self,pageIndex):
		try:
			url = 'http://www.qiushibaike.com/8hr/page/'+ str(pageIndex)+'/?s=4892985'
			#构建请求request,获取页面代码
			request = urllib2.Request(url,headers=self.headers)
			response = urllib2.urlopen(request)
			pageCode = response.read().decode("utf-8")
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print e.reason
				return None
	#获取某一页的内容并解析
	def get_pageItems(self,pageIndex):	
		content = self.get_page(pageIndex)
		soup = BeautifulSoup(content,'lxml')
		items = soup.find_all(name="div",class_="article block untagged mb15")
		#存储每页的段子
		page_list = []
		for i in items:
			haveImg = i.find("div",class_="thumb")
			if not haveImg:
				author = i.find("div",class_ = 'author clearfix')
				author = author.find(name = 'h2').get_text().strip()
				content = i.find("div",class_="content").get_text().strip()
				haoxiao = i.find("span",class_="stats-vote").get_text().strip()
				comment = i.find("span",class_="stats-comments").find("a")
				if comment != None:
					comment = comment.get_text().strip()
				else:
					comment = "none"
				#将作者，内容，好笑，评论组成一个元组，追加到list里
				c=(author,content,haoxiao,comment)
				page_list.append(c)
		return page_list
	#加载新的页面
	def load_page(self):
		#如果当前未看页数小于2页，则加载新的一页
		if self.enable == True:
			if len(self.one_page) < 2:
				#获取新的页数段子
				page_story = self.get_pageItems(self.pageIndex)
				#将该页段子存到全局列表里
				if page_story:
					self.one_page.append(page_story)
					#页码+1，表示下次读取下一页
					self.pageIndex += 1
	#打印段子，每次回车打印一个段子
	def print_oneStory(self,page_story,page):
		print u"第%d页" %page
		for story in page_story:
			#等待用户输入
			input = raw_input()
			#每次输入回车，需要判断是否加载新的页面
			self.load_page()
			#如果输出quit，则程序结束
			if input == 'quit':
				self.enable = False
				return
			print u"发布人:%s\n%s\n%s\t%s\n" %(story[0],story[1],story[2],story[3])
	#开始方法
	def start(self):
		print u"正在读取糗事百科，按回车查看新的段子，quit退出"
		#更改变量，运行程序
		self.enable = True
		#先加载一页内容
		self.load_page()
		#设置变量，控制当前读到第几页
		now_page = 0
		while self.enable:
			if len(self.one_page) > 0:
				#从全局list读取一页段子
			 	page_story = self.one_page[0]
				#当前读到页数加一
				now_page += 1
				#取出第一页后，将其在全局列表里删除
				del self.one_page[0]
				#输出该页段子
				self.print_oneStory(page_story,now_page)
qiubai = QSBK()
qiubai.start()
