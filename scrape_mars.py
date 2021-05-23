# Dependencies
from os import name
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_dict={}
    ### NASA Mars News

    # URL of page to be scraped
    url = 'https://redplanetscience.com'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html,'html.parser')

    # Retrieve the latest news title
    news_title=soup.find_all('div', class_='content_title')[0].text
    # Retrieve the latest news paragraph
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text
    
    ### JPL Mars Space Images - Featured Image

    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = "https://spaceimages-mars.com/"
    browser.visit(featured_image_url)

    # HTML object
    html = browser.html
    # Parse HTML
    soup = bs(html,"html.parser")
    # Retrieve image url
   
    
    relative_image_path = soup.find_all('img')[3]["src"]
    featured_image_url = featured_image_url + relative_image_path

    ### Mars Fact

    # Scrape Mars facts 
    url='https://galaxyfacts-mars.com/'
    tables=pd.read_html(url)
    
    mars_fact=tables[0]
    mars_fact=mars_fact.rename(columns={0:"Profile",1:"Value"},errors="raise")
    mars_fact.set_index("Profile",inplace=True)
    mars_fact
    
    fact_table=mars_fact.to_html()
    fact_table.replace('\n','')
    
    ### Mars Hemispheres

    # Scrape Mars hemisphere title and image
    base_url='https://astrogeology.usgs.gov'
    url= base_url +'/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    # Extract hemispheres item elements
    items = soup.find_all('div', class_='item')
    urls = []
    titles = []
    for item in items:
       urls.append(base_url + item.find('a')['href'])
       titles.append(item.find('h3').text.strip())
     
    browser.visit(urls[0])
    html = browser.html
    soup = bs(html, 'html.parser')
    oneurl = base_url+soup.find('img',class_='wide-image')['src']
    oneurl

    img_urls = []
    for oneurl in urls:
      browser.visit(oneurl)
      html = browser.html
      soup = bs(html, 'html.parser')
#     savetofile(textfilename,soup.prettify())
      oneurl = base_url+soup.find('img',class_='wide-image')['src']
      img_urls.append(oneurl)
    
    img_urls
            
    hemisphere_image_urls = []

    for i in range(len(titles)):
     hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

     hemisphere_image_urls
    
    for i in range(len(hemisphere_image_urls)):
     print(hemisphere_image_urls[i]['title'])
    print(hemisphere_image_urls[i]['img_url'] + '\n')
    
    # Create dictionary for all info scraped from sources above
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "fact_table":fact_table,
        "hemisphere_images":hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    return mars_dict

if __name__ == "__main__":
    md = scrape()
    print(md)