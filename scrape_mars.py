from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # Visit related web page
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Find the latest news and article overview
    news_title = soup.find('div', class_='content_title').text
    new_p = soup.find('div', class_='article_teaser_body').text


    # URL of page to be scraped for featured image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', attrs={'class':'carousel_items'})
    image_link = results.article['style']
    #remove urls unnecessary letters
    featured_image_url = image_link.replace('background-image: url(','')
    featured_image_url = featured_image_url.replace(');','')
    featured_image_url = featured_image_url[1:-1]
    featured_image_url = url + featured_image_url
    

    # URL of page to be scraped for Mars weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('p', attrs={'class':'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'})
    mars_weather = results[1].contents[0]

    # URL of page to be scraped for Mars facts
    url = "https://space-facts.com/mars/"

    #Retrieve table for Mars facts
    table = pd.read_html(url)
    df = table[1]
    df.columns = ['Dimensions', 'Value']  
    df = df.iloc[1:]
    df.set_index('Dimensions', inplace=True)

    #Convert data to html string
    mars_table = df.to_html()
    mars_table = mars_table.replace('\n', '') 

    # URL of page to be to find Mars Hemispheres images
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', attrs={'class':'description'})

    #Find Mars Hemispheres titles
    hemispheres = []
    for result in results:
        hem = result.find('h3').text
        hemispheres.append(hem)
    # Loop to find the page that containes hem full sized images
    link_hem = []
    for result in results:
        img = result.find('a')['href']
        link_hem.append('https://astrogeology.usgs.gov' + img)

    # use browser.visit in loop to go through each hem page to find image links
    hemisphere_image_urls = []
    for link in link_hem:
        browser.visit(link)
        soup = bs(browser.html,"html.parser")
        li = soup.find('li')
        link = li.find('a')
        href = link['href']
        hemisphere_image_urls.append(href)

    #Store data in dictionary
    mars_data = {
        'news_title': news_title,
        'news_overview': new_p,
        'featured_image':featured_image_url,
        'mars_weather': mars_weather,
        'mars_dimensions': mars_table,
        'mars_hemisphere': hemispheres,
        'mars_hemisphere url': hemisphere_image_urls
    }

    #Close the browser after scraping
    browser.quit()

    #Return results
    return mars_data