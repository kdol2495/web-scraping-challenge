# dependencies
import pandas as import pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests

# chromedriver and browser connection
executable_path = {'executable_path': 'C:\Users\kdola\Downloads\chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# overall scrape
def scrape():
    mars_data = {}
    output = marsNews()
    mars_data["mars_news"] = output[0]
    mars_data["mars_paragraph"] = output[1]
    mars_data["mars_image"] = marsImage()
    mars_data["mars_weather"] = marsWeather()
    mars_data["mars_facts"] = marsFacts()
    mars_data["mars_hemisphere"] = marsHem()

    return mars_data
# image scrape
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

# news scrape
def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output

  
# facts scrape
def marsFacts():
    import pandas as pd
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts

# hemispheres scrape
def marsHem():
    import time 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)
    return mars_hemisphere

# weather tweet scrape
def marsWeather():
    # last tweet url
    tweet_url = 'https://twitter.com/MarsWxReport/status/1198749371459870722'
    browser.visit(tweet_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    return mars_weather




