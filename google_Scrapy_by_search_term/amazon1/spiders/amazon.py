#-*- coding: utf-8 -*-
# any thing you want
from operator import le
import re
import selectors
from time import time
import scrapy
import sys
import random
import requests
from bs4 import BeautifulSoup

 


class AmazonSpider(scrapy.Spider):
    name = 'amazonsearchterm'
 
    abc=open('/home/moglix/Desktop/amazonsearchterm.txt').read().splitlines()
    data_analysy={}
    for intercept_url in abc:
            ur_l=intercept_url
            base_url=ur_l.split('||')[0]
            msn_url=ur_l.split('||')[1]
            data_analysy[base_url]=msn_url
            #print(base_url,msn_url)

    start_urls=data_analysy.keys()

    #start_urls=abc
    
    def parse(self, response):
        data={}
        # print("start scrapping",response.css('.jtfYYd').getall() )
        r1=(response.xpath("//div[contains(@class,'a-section')]/div[contains(@class,'sg-row')]")).getall()
        google_search=(response.xpath("//div[contains(@class,'yuRUbf')]/a")).getall()

        # print("google_search ",google_search)
        #r1=(response.xpath("//a[contains(@class,'a-link-normal s-no-outline')]/@href")).getall()
        print(len(google_search))
        if(len(r1)==1):
            r1=(response.xpath("//div[contains(@class,'a-section a-spacing-base')]")).getall()

        p_id=''
        substring="/dp"
        amazon_string="amazon"
        sub_sponsered="Sponsored"
        amzaon_url="https://www.amazon.in/product-reviews/"
        filter_url="?filterByStar=positive&reviewerType=all_reviews&pageNumber=1"
        response_urls=response.url.replace('%20',' ')
        msn_urls=AmazonSpider.data_analysy[response_urls]
        #add failed urls 
        failed_urls=response_urls+"||"+msn_urls
        if(len(google_search)==0):
           google_search_result=requests.get(failed_urls)
           soup=BeautifulSoup(google_search_result.text,'html.parser')
        #    print(soup.prettify())
           search_results=soup.select('a')
           for href_link in search_results:
            #    print(href_link.get('href'))
               href_string_value=href_link.get('href')
               if(amazon_string in href_string_value):
                print("amazon_string :" ,href_string_value)
                amazon_url=re.split("&sa",href_string_value)[0]
                print(amazon_url)
                if(substring in amazon_url):
                    splited_amzaon_url=re.split("dp/",amazon_url)[1]
                # splited_amzaon_url=re.split("/url?q=",amazon_url)[0]
                    p_id=amzaon_url+splited_amzaon_url.strip()+filter_url+"||"+msn_urls
                    print("splited_amzaon_url ",p_id)
        # print("search_results ",search_results)
        intem_start=0
        print("lenght of data scrapped",len(google_search))
        if(len(google_search)>=1 and len(p_id)==0):
         for link in google_search:
            # print("link ",link)
            if amazon_string in link:
                href_string=re.split("data-ved",link)[0]
                href_string1=re.split("href=",href_string)[1].replace('"','')
                print("String ",href_string1)
                if(substring in href_string1):
                  product_id=re.split("dp/",href_string1)[1]
                  print(href_string1)
                  p_id=amzaon_url+product_id.strip()+filter_url+"||"+msn_urls
                  print("amazon url along with msn : ",p_id)


    


        # for ret in r1:
        #       if substring in ret:
        #        #print(intem_start)
        #        if intem_start <len(r1): 
        #          pid_str=re.split('dp/',ret)[1]
        #          product_id=re.split('/ref',pid_str)[0]
        #          if product_id in p_id:
        #            #print("exist "+product_id)
        #            continue
        #          else:
        #              #print("hellao "+ret)
        #              #check the prdouctID is sponsered or not
        #              if sub_sponsered in ret:
        #                  print( " id sponsered sponserd ")
        #                  continue
        #              else:
        #                  intem_start=intem_start+1
        #                  print("intem_start",intem_start)
        #                  if(len(p_id)==0):
        #                      #capture the url first_four_word_count
        #                       u_R_L=response.url.split('k=')[1].replace('%20',' ')
        #                       #print("U_R_L",u_R_L)
        #                       #capture word count 
        #                       word_count=len(u_R_L.split())
        #                       print("word_count",word_count)
        #                       if(float(word_count)>=1):
        #                           words_count_array=u_R_L.split(' ')
        #                           searc_items_words=''
        #                           index=0
        #                           for w in words_count_array:
        #                               if(index==0):
        #                                   searc_items_words=w
        #                               if(index>0 and index <=2):
        #                                   if("boAt" in ret):
        #                                       print("Boat")
        #                                       searc_items_words=searc_items_words+' '+w
        #                                   else:
        #                                       searc_items_words=searc_items_words+' '+w
        #                                       print(" ret :" ,ret)
        #                                       if("Sony" in ret or "Zebronics" in ret):
        #                                          index=index+1
        #                               index=index+1
        #                           if("In" in searc_items_words):
        #                               searc_items_words=searc_items_words.replace('In','')
        #                           if("in" in searc_items_words):
        #                               searc_items_words=searc_items_words.replace('in','')
        #                           print("word should present in ",searc_items_words)
        #                           if(searc_items_words in ret):
        #                              print(searc_items_words)   
        #                              p_id=amzaon_url+product_id.strip()+filter_url+"||"+msn_urls
        #                              print("Non Sponsered productId"+p_id)
                         
        #        else:
        #            #print("break")
        #            break
        #add to failed url
        #print(len(p_id))
        if len(p_id)==0 :
             filet=open('failed_netmart.txt','a')
             filet.write(str(failed_urls)+"\n")
        
        data={
            'Product_Id':p_id,
            'url':response.url
            
        }
        
        yield data

