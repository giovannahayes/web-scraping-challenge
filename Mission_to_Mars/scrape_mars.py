# dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import pymongo

urls = {
        'news': 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest',
        'image': 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars',
        'facts' : 'https://space-facts.com/mars/',
        'hemi' : 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

def request_soup(url):
    # get page with requests module
    response = requests.get(url)
    # create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup


def init_browser():
    
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    # Mars News: Get title and paragraph for latest article
    # get page with requests module
    response = requests.get(urls['news'])
    # create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find('div', class_="content_title").a.text.strip()
    news_paragraph = soup.find('div', class_="article_teaser_body").text.strip()


    # Mars Images : Get the latest featured image title and image url 
    # navigage to correct page     
    browser = init_browser()
    browser.visit(urls['image'])
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    # create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # parse soup object 
    feat_img = soup.find('figure', class_='lede')

    # modify relative to absolute url 
    featured_image_url = f'https://www.jpl.nasa.gov{feat_img.a.img["src"]}'


    # Mars Facts: pandas to read the html table data into a list of dictionaries
    tables = pd.read_html(urls['facts'])

    # convert dictionary in the list into dataframe and name columns
    df = tables[0]
    df.columns = ['Parameter', 'Value']
    df.set_index('Parameter', inplace=True)

    # convert the dataframe into an html table, strip the end of line 
    # put output into html file
    fact_table = df.to_html()
    fact_table = fact_table.replace('\n', '')
 

    
    # # Mars Hemispheres Images
    # browser = init_browser()
    # browser.visit(urls['hemi'])

    # # get page html and make beautifulsoup object
    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')

    # # get html containing the titles and put into a list
    # title_list = soup.find_all('div', class_='description')

    # # Loop through the div objects and scrape titles and urls of hires images
    # # create the list to store dictionaries
    # hemisphere_image_urls = []
    # for title in title_list:
        
    #     browser.visit(urls['hemi'])
    #     browser.click_link_by_partial_text(title.a.h3.text)
        
    #     html = browser.html
    #     soup = BeautifulSoup(html, 'html.parser')

    #     img_url_list = soup.find('img', class_='wide-image')
    #     img_url = f"https://astrogeology.usgs.gov{img_url_list['src']}"

    #     post = {
    #             'title': title.a.h3.text,
    #             'image_url': img_url
    #             }
    #     hemisphere_image_urls.append(post)

    

    # input into mars_data dictionary to hold all values to be entered into mongo db
    mars_data = {
            'news_title': news_title,
            'news_paragraph': news_paragraph,
            'featured_image_url': featured_image_url,
            'fact_table': fact_table,
            # 'hemisphere_image_urls': hemisphere_image_urls
    }
    print(mars_data)
    return mars_data