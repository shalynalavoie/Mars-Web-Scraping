# Dependencies
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
    url= base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    # Extract hemispheres item elements
    mars_hems=soup.find('div',class_='collapsible results')
    mars_item=mars_hems.find_all('div',class_='item')
    hemisphere_image_urls=[]

    # Loop through each hemisphere item
    for item in mars_item:
        # Error handling
        try:
            # Extract title
            hem=item.find('div',class_='description')
            title=hem.h3.text
            # Extract image url
            hem_url=hem.a['href']
            browser.visit(usgs_url+hem_url)
            html=browser.html
            soup=bs(html,'html.parser')
            image_src=soup.find('li').a['href']
            if (title and image_src):
                # Print results
                print('-'*50)
                print(title)
                print(image_src)
            # Create dictionary for title and url
            hem_dict={
                'title':title,
                'image_url':image_src
            }
            hemisphere_image_urls.append(hem_dict)
        except Exception as e:
            print(e)

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

