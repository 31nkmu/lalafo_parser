import json
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

URL = 'https://lalafo.kg/sitemap'
options = Options()
ua = UserAgent()
options.add_argument(f'user-agent={ua.chrome}')
options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')

links = []


def get_category_links(url):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(2)
        site_map = driver.find_element(By.CLASS_NAME, value='sitemap')
        categories = site_map.find_elements(By.CLASS_NAME, value='sitemap__subcategory-name')
        for category in categories:
            links.append({
                'title': category.text,
                'link': category.get_attribute('href')
            })
            if 'Бюро находок' in category.text:
                break
        return links
    except Exception as ex:
        return ex
    finally:
        driver.close()
        driver.quit()


def write_json(data):
    with open('category_links.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
