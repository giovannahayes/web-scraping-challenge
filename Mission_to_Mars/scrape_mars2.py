import requests
import bs4
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

def scrape():
    # start browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    nasa_url = 'https://mars.nasa.gov/news/?page=0'
    browser.visit(nasa_url)
    
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find('ul', class_='item_list')
    news_title = articles.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    # JPL Mars Space Images
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    time.sleep(5)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    header = soup.find('div', class_='carousel_container')
    feature_pic = header.find('article')
    pic_background = feature_pic['style']
    pic_id = pic_background[53:61]
    featured_image_url = f'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA24152_hires.jpg'

    # Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    tweets = soup.find('div', class_="css-1dbjc4n")
    mars_weather = tweets.find('div', lang='en').text

    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    all_tables = pd.read_html(facts_url)
    mars_facts_table = all_tables[0]
    mars_facts_table.columns = ["Description", "Value"]

    table_html = mars_facts_table.to_html()

    # Mars Hemispheres
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    all_hemispheres = soup.find('div', class_='collapsible results')
    hemispheres = all_hemispheres.find_all('div', class_='item')

    beginning_url = 'https://astrogeology.usgs.gov'

    hemisphere_image_urls = []

    for result in hemispheres:
        hemisphere = result.find('div', class_="description")
        title = hemisphere.h3.text

        ending_url = hemisphere.a["href"]    
        browser.visit(beginning_url + ending_url)

        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')

        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = image_url

        hemisphere_image_urls.append(hemisphere_dict)
    
    # Collect Data into one dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": table_html,
        "hemispheres_images": hemisphere_image_urls
    }

    return mars_dict