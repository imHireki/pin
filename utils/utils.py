from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas
import time
import json


def setup_driver():
    driver_options = webdriver.FirefoxOptions()
    driver_options.headless = True

    return webdriver.Firefox(
        options=driver_options
        )

def scroller(driver, scrolls): 
    while scrolls > 1:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
            )
        time.sleep(10)
        scrolls -= 1

def write_to_json(data):
    w_file = open('data.json', 'w')
    json.dump(data, w_file, indent=4)
    w_file.close() 

def current_json_data():  
    r_file = open('data.json', 'r')
    json_data = json.load(r_file)
    r_file.close()
    return json_data

def get_searched_links(driver):
    try:
        collection = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.Collection')
                )
            ).get_attribute('outerHTML')
    except Exception:
        raise Exception('Problem getting the links')

    # soup
    collection_soup = BeautifulSoup(collection, 'html.parser')
    link_tags = collection_soup.find_all('a')

    PINTEREST_URL = 'https://br.pinterest.com'
    pin_urls = []

    # append urls to pin_urls
    for link in link_tags:
        pin_href = link.get('href')
        url = f'{PINTEREST_URL}{pin_href}' 
        pin_urls.append(url)
    return pin_urls

def get_titles_section(driver): 
    try:
        return WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.rDA:nth-child(1)')
                )
            ).get_attribute('outerHTML')
    except Exception:
        return None

def get_title(section):
    if not section:
        return ''
    return BeautifulSoup(section, 'html.parser').h1.string

def get_subtitle(section):
    if not section:
        return ''
    
    soup = BeautifulSoup(section, 'html.parser')
    try:
        return soup.h2.string
    except Exception as e:
        return ''

def get_tags_section(driver): 
    try:
        return WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[2]/di'\
                           'v/div/div/div[2]/div/div/div/div/div[2]/div/di'\
                           'v/div/div[7]')
                )
            ).get_attribute('outerHTML')
    except Exception:
        return None

def get_tags(section):
    if not section:
        return []

    a_tags = BeautifulSoup(section, 'html.parser').find_all('a')
    tags = []
    for tag in a_tags:
        tag_soup = BeautifulSoup(str(tag), 'html.parser')
        tags.append(tag_soup.a.string) 
    return tags     

def get_image_section(driver):
    try:
        return WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.PcK > div:nth-child(1)'\
                                  ' > img:nth-child(1)')
                )
            ).get_attribute('outerHTML')
    except Exception:
        return None

def get_image(section):
    if not section:
        return ''
    return BeautifulSoup(section, 'html.parser').img.get('src', '')

def validate_data(data):
    """ errors if not img and not title """
    # def data
    title = data.get('title', '')
    subtitle = data.get('subtitle', '') 
    tags = data.get('tags', [])
    image = data.get('image', '')
    errors = {}

    # Check / patch data - TODO: Update it to regex
    if title == 'requests are open!':  # pinterest placeholder
        title = ''
     
    if subtitle == ' ' or subtitle == None:
        subtitle = ''
     
    if not image:
        errors['image'] = 'lack in image'

    # Try patch the title
    if not title:
        if subtitle:
            title = subtitle
        elif tags:
            title = tags[0] 
        else:
            errors['title'] = 'lack in title'
             
    # Join the new data
    cleaned_data = {
        'title': title,
        'subtitle': subtitle,
        'tags': tags,
        'image': image
        }
    
    return cleaned_data, errors   
 