#coding=utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import unicodedata
from csv import DictWriter
import os
import requests
import traceback
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')   #主要是该条
options.add_argument('--ignore-ssl-errors')
chromeOptions = webdriver.ChromeOptions()
class DoubanParser:
    driver = webdriver.Chrome()
    records = []
    records_error = []
    def get_proxy(Any):
        return requests.get("http://127.0.0.1:5010/get/").json()

    def delete_proxy(proxy,Any):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

    def getHtml(self,url):
    # ....
        retry_count = 5
        proxy = self.get_proxy().get("proxy")
        chromeOptions.add_argument("--proxy-server=http://"+proxy)
        browser = webdriver.Chrome(chrome_options = chromeOptions)
        while retry_count > 0:
            try:
                self.driver.get(url)
                # 使用代理访问
                html = self.driver.page_source
                return html
            except Exception:
                retry_count -= 1
        # 删除代理池中代理
        self.delete_proxy(proxy)
        return None

    def parse(self,page_url): 
        try:
            html = self.getHtml(page_url)
            while(html == None):
                html = self.getHtml(page_url)
            page_soup = BeautifulSoup(html,features='lxml')
            movie_titles = page_soup.find('div',{'id':'wrapper'})
            title = movie_titles.h1.span.string##title : #wrapper > h1 > span
            
            book_rating = page_soup.find('div',{'class':'rating_self clearfix'})##interest_sectl > div > div.rating_self.clearfix > strong
            rating =  book_rating.strong.get_text();
            
            author = page_soup.find('div',{'id':'info'}).select('span')[0].a##info > span:nth-child(1) > a
            
            book_summary = page_soup.find('div',{'id':'link-report'})
            summary = book_summary.find('span',{'class':'all hidden'}).div.div.p.get_text()#link-report > span.all.hidden > div > div > p
            #summary = ''.join(summary.split())##剔除空格与换行符
            summary = summary.replace("\u3000",'')
            summary = summary.replace(' ','')
            summary = summary.replace('\n','')
            author_summary= page_soup.find('div',{'class':'related_info'}).select('div')[5].div.div.p.string#content > div > div.article > div.related_info > div:nth-child(5) > div > div > p
            movie_dict = {'book':title,'rating':rating,'link':page_url,'book summary':summary,'author summary':author_summary}
            self.records.append(movie_dict)
        except:
            movie_dict = {'book':"ERROR",'rating':"ERROR",'link':page_url,'book summary':traceback.format_exc(),'author summary':"ERROR"}
            self.records_error.append(movie_dict)
    def read_txt(self):
        num = 1
        f = open("D:/360MoveData/Users/admin/Desktop/coursework/web_info/lab/lab1/Book_id.txt")
        byt = f.readlines()
        for line in byt:
            url = "https://book.douban.com/subject/"+line
            self.parse(url)
            print(num,"has been resolved")
            num =num + 1
        '''url = "https://book.douban.com/subject/1046265"
        self.parse(url)'''
        if os.path.exists("douban_book.csv"):
            os.remove("douban_book.csv")
        with open('douban_book.csv','w', newline='', encoding='utf-8-sig') as file:
            headers = [key for key in self.records[0].keys()]
            csv_writer = DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            for record in self.records:
                csv_writer.writerow(record)
        if self.records_error != []:
            with open('douban_book_ERROR.csv','w', newline='', encoding='utf-8-sig') as file:
                headers = [key for key in self.records_error[0].keys()]
                csv_writer = DictWriter(file, fieldnames=headers)
                csv_writer.writeheader()
                for record in self.records_error:
                    csv_writer.writerow(record)
    
parser=DoubanParser()
parser.read_txt()