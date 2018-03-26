__author__ = 'mzw'
# -*- coding:utf-8 -*-
# copy from cqc
import urllib2
import cookielib
import urllib
import re


class Qs:
    def __init__(self):
        self.page = 1
        self.user_agent = 'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
        self.headers = {'user-Agent': self.user_agent}
        self.stories = []
        self.enable = False


    def getpage(self, page):
        try:
            url = "https://www.qiushibaike.com/hot/page/" + str(self.page)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            PageCode = response.read().decode('utf-8')
            return PageCode

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "wrong", e.reason
                return None


    def getPageItems(self, page):
        content = self.getpage(page)
        pattern = re.compile('<h2>(.*?)</h2>.*?<a.*?<div.*?<span>(.*?)</span>.*?<i.*?>(.*?)</i>.*?<i.*?>(.*?)</i>',
                             re.S)
        items = re.findall(pattern, content)
        pageStories = []
        for item in items:
            pageStories.append([item[0], item[1], item[2], item[3]])
        return pageStories


    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.page)
                if pageStories:
                    self.stories.append(pageStories )
                    self.page += 1


    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print story[0],story[1],story[2],story[3]

    def start(self):
        print "start,press enter to continue or press q to quit"
        self.enable = True
        self.loadPage()
        print self.page

        nowPage = 0
        while self.enable == True:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)


ss = Qs()
ss.start()
