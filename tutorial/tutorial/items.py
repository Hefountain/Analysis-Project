# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
# define the fields for your item here like:
# 用户名
	user_name = scrapy.Field()
	# 评论时
	comment_time = scrapy.Field()
	# 评分
	score = scrapy.Field()
	# 认为有用的人数
	agree_num = scrapy.Field()
	# 影
	comment = scrapy.Field()
	# 是否看过
	is_view = scrapy.Field()