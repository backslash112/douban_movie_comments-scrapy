import scrapy
from douban_movie_comments.items import CommentItem
from douban_movie_comments.settings import *
import re

class CommentItem(scrapy.Spider):
    name = "comments"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/subject/26284595/comments?sort=time"]


    # https://movie.douban.com/subject/26284595/comments?start=20&limit=20&sort=new_score // page 2
    # https://movie.douban.com/subject/26284595/comments?start=40&limit=20&sort=new_score // page 3
    headers = HEADERS

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, headers=self.headers, callback=self.parse)


    def parse(self, response):
        self.parse_comments(response)

    def parse_comments(self, response):
        div_comments = response.xpath('//div[@class="comment"]')
        for div_comment in div_comments:
            comment = div_comment.xpath('p/text()').extract_first()
            rate_txt = div_comment.xpath('h3/span[@class="comment-info"]/span')[0].xpath('@class').extract_first()
            rate = re.findall(r'\d+', rate_txt)
            if rate:
                print(str((int(rate[0])/10)) + ": " + comment.rstrip())
            else:
                print("1.0: " + comment.rstrip())
