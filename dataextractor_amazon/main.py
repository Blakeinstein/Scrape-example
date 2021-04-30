from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import csv

# about the data
RATING = re.compile("[0-9]\.[0-9] out of 5 stars")
DELIVERY = re.compile("Get it by (.*)")

DATA_FIELDS = ["Product Name",
              "Product URL",
              "Image URL",
              "Old Price",
              "Deal Price",
              "Rating",
              "Number of Ratings",
              "Delivery Date"]

URL = "https://amzn.to/3sYcOs5"

MIN_COUNT = 50

OUTPUT = "output.csv"

def main():
    # Setup selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-features=NetworkService")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    DRIVER = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    DRIVER.maximize_window()
    
    # fetch page
    DRIVER.get(URL)
    DRIVER.implicitly_wait(10)
    
    # setup data-storage
    data_set = []
        
    # fetch data
    page_no = 1
    ids = set()
    count = 0
    while page_no < 6 and count < MIN_COUNT and DRIVER.find_element_by_css_selector('[data-component-type="s-search-results"]'):
        print(f"Navigating page {page_no}")
        
        # wait for page load
        while True:
            try:
                DRIVER.find_element_by_css_selector('.aok-hidden>.a-spinner-wrapper')
                break
            except NoSuchElementException:
                continue
        
        element = DRIVER.find_element_by_css_selector('[data-component-type="s-search-results"]')
        soup = BeautifulSoup(element.get_attribute('innerHTML'), features="html.parser")
        entries = soup.findAll('div', {'data-component-type': "s-search-result"})
        for entry in entries:
            id = entry['data-asin']
            if id in ids:
                continue
            ids.add(id)
            print(f"Getting info about {id}, current count: {count}")
            
            try:
                # get elements
                img = entry.find('img')
                rating = entry.find('span', {'aria-label': RATING})
                dmatch = DELIVERY.search(entry.find('span', {'aria-label': DELIVERY})['aria-label'])
                
                # ad check
                name = img['alt']
                if name.startswith('Sponsored Ad'):
                    continue
                # add data
                data = dict()
                data['Product Name'] = name
                data['Product URL'] = "https://amazon.in" + img.parent.parent['href']
                data['Image URL'] = img['src']
                data['Old Price'] = entry.select('.a-price.a-text-price>span')[0].get_text()[1:]
                data['Deal Price'] = entry.select('.a-price-whole')[0].get_text()
                data['Rating'] = rating['aria-label']
                data['Number of Ratings'] = rating.next_sibling['aria-label']
                data['Delivery Date'] = dmatch.group(1)
            except:
                continue
            
            data_set.append(data)
            count += 1 
            
            
        # try for next page
        try:
            DRIVER.find_element_by_css_selector('.a-last>a').click()
        except NoSuchElementException:
            break
        finally:
            DRIVER.implicitly_wait(10)
            page_no += 1
        
    DRIVER.quit()
    
    # write
    try:
        with open(OUTPUT, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=DATA_FIELDS, lineterminator='\n')
            writer.writeheader()
            for data in data_set:
                writer.writerow(data)
    except IOError:
        print("I/O error")

if __name__ == "__main__":
    main()