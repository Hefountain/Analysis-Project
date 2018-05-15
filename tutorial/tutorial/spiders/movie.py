# -*- coding: utf-8 -*-
import scrapy
import string
import random
from tutorial.items import TutorialItem

class MovieSpider(scrapy.Spider):
	name = 'movie'
	allowed_domains = ['movie.douban.com']
	start_urls = [
	# 看过
	'https://movie.douban.com/subject/4920389/comments?status=P',
	# 想看
	'https://movie.douban.com/subject/4920389/comments?status=F'
	]

	headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"Host": "movie.douban.com",
	"Referer": "https://movie.douban.com/",
	"Upgrade-Insecure-Requests": "1",
	"Content-Type": "text/html; charset=utf-8",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
	}

	cookie = 'bid=84YirbK3vIQ; gr_user_id=b9c1a4c3-0609-4eb3-8201-ef0b2db89017; _vwo_uuid_v2=D4CBF11AA6337436F7FD362A2DADA20BA|71b3349fa3fbe3bcc367e3b491ff2774; viewed="26677686_6816154_2995812_1770782"; __utmc=30149280; __utmc=223695111; ll="118286"; __yadk_uid=94vtxPuHQmua179cPQiZEzZLtJHOlhBC; ap=1; ct=y; ps=y; ue="zweite@163.com"; push_doumail_num=0; dbcl2="81183949:d4Zlanu06Ek"; ck=ANgn; __utmz=30149280.1526312405.15.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utmz=223695111.1526312405.10.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; push_noty_num=0; __utmv=30149280.8118; _pk_ses.100001.4cf6=*; __utma=30149280.1365985001.1517911650.1526352305.1526354685.18; __utmb=30149280.0.10.1526354685; __utma=223695111.2033577237.1525445655.1526352305.1526354685.13; __utmb=223695111.0.10.1526354685; _pk_id.100001.4cf6=4cbe0c39227bb53f.1525445654.13.1526354793.1526352776.'
	cookies = {}

	def web_login(self):
		kvs = self.cookie.split(";")
		for kv in kvs:
			kk = kv.split("=")
			self.cookies[kk[0]] = kk[1]
		return

	def start_requests(self):
		self.web_login()
		print self.cookies
		for url in self.start_urls:
			self.cookies["bid"] = "".join(random.sample(string.ascii_letters + string.digits, 11))
			yield scrapy.Request(url, headers=self.headers, cookies=self.cookies)


	def parse(self, response):
		next_page_url = response.xpath('//a[@class="next"]/@href').extract_first()
		print "heiheiheihei" + next_page_url
		if next_page_url is not None:
			self.cookies["bid"] = "".join(random.sample(string.ascii_letters + string.digits, 11))
			yield scrapy.Request("https://movie.douban.com/subject/4920389/comments" + next_page_url, headers=self.headers, cookies=self.cookies, callback=self.parse)

		for node in response.xpath('//div[@class="comment-item"]'):
			item = TutorialItem()
			item['comment'] = node.xpath('.//div/p/text()').extract_first().encode(encoding='UTF-8')
			item['comment_time'] = node.xpath('.//span[@class="comment-time "]/@title').extract_first()
			item['user_name'] = node.xpath('.//span[@class="comment-info"]/a/text()').extract_first()
			item['agree_num'] = node.xpath('.//span[@class="votes"]/text()').extract_first()
			infos = node.xpath('.//span[@class="comment-info"]/span')
			isView = node.xpath('.//span[@class="comment-info"]/span/text()').extract_first()
			
			item['is_view'] = isView 
			if isView==u'看过':
				if len(infos) == 2:
					item['score'] = u"无评分"
				else:
					item['score'] = node.xpath('.//span[@class="comment-info"]/span[2]/@title').extract_first()
			else:
				item['score'] = u'无评分'
			yield item




