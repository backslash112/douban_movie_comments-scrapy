import scrapy
from douban_movie_comments.items import CommentItem
from douban_movie_comments.settings import *
import re
import logging

class CommentSpider(scrapy.Spider):
    name = "comments"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/subject/26284595/comments?start=1415&limit=20&sort=new_score"]

    headers = HEADERS
    cookies = COOKIES

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        logging.info("{0}: {1}.".format(response.status, response.url))
        if response.status != 200:
            print('return because != 200')

        # Get data from response object
        div_comments = response.xpath('//div[@class="comment"]')
        for div_comment in div_comments:
            comment = div_comment.xpath('p/text()').extract_first()
            rate_txt = div_comment.xpath('h3/span[@class="comment-info"]/span')[0].xpath('@class').extract_first()
            rate_str = re.findall(r'\d+', rate_txt)
            if rate_str:
                rate = int(rate_str[0])/10
            else:
                rate = 0

            item = CommentItem()
            item['rate'] = rate
            item['comment'] = comment.rstrip()
            yield item

        # Find next page url and send a new request with it
        next_url = response.css('.next').xpath('@href').extract_first()
        if not next_url:
            logging.warning("No next url anymore!")
            return
        bash_url = "https://movie.douban.com/subject/26284595/comments"
        yield scrapy.Request(bash_url + next_url, headers=self.headers, cookies=self.cookies, callback=self.parse)
