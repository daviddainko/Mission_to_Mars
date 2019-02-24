from selenium import webdriver
from bs4 import BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from pymongo import MongoClient

def init_browser():
    executable_path = {'executable_path': '/Users/davidcdainko/Desktop/Northwestern/NUCHI201811DATA2//chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_info = {}

    #NASA Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = bs(html,"html.parser")

    title = soup.find('div', class_='content_title').text
    para = soup.find('div', class_='article_teaser_body').text

    mars_info['news_title'] = title
    mars_info['news_paragraph'] = para

    # return mars_info


# def scrape_images():
    #JPL Mars Space Images - Featured Image
    # browser = init_browser()
    # mars_info = {}

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html,"html.parser")

    article = soup.find('article', class_='carousel_item')
    style = article['style']

    featured_image_url = style.replace("background-image: url(\'","https://www.jpl.nasa.gov")
    featured_image_url = featured_image_url.replace("');","")

    mars_info['mars_featured_image'] = featured_image_url    
    
    # return mars_info

# def scrape_weather():
    #Mars Weather
    # browser = init_browser()
    # mars_info = {}

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html,"html.parser")

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    mars_info['mars_weather'] = mars_weather
    
    # return mars_info

# def scrape_facts():
#     #Mars Facts
#     browser = init_browser()
#     mars_info = {}

    client = MongoClient()
    client = MongoClient('Mongo URI')
    # select database
    db = client['database']
    test = db.test

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html,"html.parser")

    facts = pd.read_html(facts_url)
    table = facts[0]
    table.columns = ['Parameter','Values']
    # table['Values'] = table.Values.apply(str)
    # table['Parameter'] = table.Parameter.apply(str)
    table = table.set_index(['Parameter'])
    clean_table = table.to_html()
    clean_table = clean_table.replace('\n','')

    mars_info['mars_facts_table'] = clean_table 

    # return mars_info


# def scrape_hemi():
#     #Mars Hemispheres
#     browser = init_browser()
#     mars_info = {}

    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')

    divs = soup.find_all('div', class_='item')
    hem_url_dict = []
    url_beginning = 'https://astrogeology.usgs.gov/'

    for div in divs:
        title = div.find('h3').text 
        image = div.find('img', class_='thumb')
        src = image['src']
        img_url = url_beginning + src
    
        hem_url_dict.append({'title':title, 'img_url':img_url})

    mars_info['hemisphere_images'] = hem_url_dict

    return mars_info
    