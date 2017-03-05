import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from bs4 import BeautifulSoup
import bs4
from scrapy.conf import settings
import sys
import re
import json



sys.setrecursionlimit(10000)


class YTPakSpider(scrapy.Spider):
    name = "YTPak"
    start_urls = ['https://www.ytpak.com/']
    custom_settings = {
        'DEPTH_LIMIT' : 0
    }

    def parse(self, response):
        print("Existing settings: %s" % self.settings['DEPTH_LIMIT'])
        formdata = {'q': 'The kapil Sharma Show'}
        yield FormRequest.from_response(response,
                                        formdata=formdata,
                                        clickdata={'type': 'submit'},
                                        callback=self.parseSearch)
    def parseSearch(self, response):
        html = response.body
        soup = BeautifulSoup(html, "lxml")
        results_group = soup.find(id="results-group")

        for res_item in results_group.contents:
            if type(res_item) is bs4.element.Tag:
                title_with_link = res_item.find('h3')
                title = title_with_link.find('a').text
                link = title_with_link.find('a')['href']
                yield scrapy.Request("http:" +  link, callback=self.parseVideoPage)
    
    def parseVideoPage(self, response):
        html = response.body
        soup = BeautifulSoup(html, "lxml")
        
        title = soup.find(class_="page-header").h3
        #print title.text

        stats_div = soup.find(class_="font-size-16")
        views = stats_div.text
        #print views

        likes_dislikes_div = soup.find(class_="font-size-13")
        likes_dislikes_spans = likes_dislikes_div.find_all("span")
        likes = likes_dislikes_spans[0].text
        dislikes = likes_dislikes_spans[1].text
        #print likes, dislikes

        about_tab = soup.find(id="aboutTab")
        publishing_date = about_tab.h4.text
        #print publishing_date
        
        description = about_tab.find(id = "videoDescriptions").text
        #print description
        
        video_id = response.url.split("v=")[1]
        #print video_id
        
        yield {
            "id" :  video_id ,
            "type" : "meta",
            "data" : {
                "title" : title.text,
                "views" : views,
                "likes" : likes,
                "dislikes" :  dislikes,
                "date" : publishing_date,
                "description" :  description
            }
        } 

        #comments
        yield scrapy.Request("https://www.ytpak.com/?component=video&task=comments&id=" + video_id , callback=self.parseComments)
        
        #sugesstions
        yield scrapy.Request("https://www.ytpak.com/?component=video&task=get-related-videos-ajax&videoid=" + video_id + "&devicetype=computer" , callback=self.parseSugessted)

    def parseComments(self, response):
        video_id = response.url.split("id=")[1]
        comments_dict = {}

        ajaxResponce = response.body
        html = json.loads(ajaxResponce)["html"]
        soup = BeautifulSoup(html, "lxml")
        comment_blocks = soup.find_all(class_ = "media-body")
        for item in comment_blocks:
            name = item.find(class_ = "media-heading").find("a").text            
            comment = item.p.text
            comments_dict[name] = comment
        yield {
            "id" :  video_id ,
            "type" : "comments",
            "data" : comments_dict 
            }    

    def parseSugessted(self, response):
        video_id = response.url.split("id=")[1].split("&")[0]
        ajaxResponce = response.body
        html = json.loads(ajaxResponce)["html"]
        soup = BeautifulSoup(html, "lxml")
        suggested_items = soup.find_all(class_ = "list-group-item quickViewContainer")
        for item in suggested_items:
            link = item.a["href"]
            yield scrapy.Request("https:" + link, callback=self.parseVideoPage)