from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
def scrape_info():
    browser = init_browser()

    # Visit realted web page
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Find the featured image
    relative_image_path = soup.find_all('img')['src']
    featured_image_url = url + relative_image_path

    #Store data in dictionary
    mars_data = {
        "featured_image_url": featured_image_url
    }

    #Close the browser after scraping
    browser.quit()

    #Return results
    return mars_data