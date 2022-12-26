import json
import os
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

ua = UserAgent()
options = Options()
options.add_argument(f'user-agent={ua.chrome}')
options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')


def write_product_json(data, file_name):
    with open(f'media/{file_name}.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_product_data(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(4)

    product_container = driver.find_element(By.CLASS_NAME, value='virtual-scroll__container')
    data = []
    products = product_container.find_elements(By.CLASS_NAME, value='AdTileHorizontal')

    for product in products:
        link_bloc = product.find_element(By.CLASS_NAME, value='AdTileHorizontalTitle')
        link = link_bloc.get_attribute('href')
        data.append({
            'text': product.text,
            'link': link
        })

    while True:
        product_container = driver.find_element(By.CLASS_NAME, value='virtual-scroll__container')
        for product in products:
            link_bloc = product.find_element(By.CLASS_NAME, value='AdTileHorizontalTitle')
            link = link_bloc.get_attribute('href')
            data.append({
                'text': product.text,
                'link': link
            })

        ActionChains(driver).scroll_to_element(products[-1]).perform()
        if products == product_container.find_elements(By.CLASS_NAME, value='AdTileHorizontal'):
            driver.execute_script("window.scrollBy(0, 250);")
            time.sleep(2)
            driver.execute_script("window.scrollBy(0, 250);")

            if products[-1] == product_container.find_elements(By.CLASS_NAME, value='AdTileHorizontal')[-1]:
                break
        products = product_container.find_elements(By.CLASS_NAME, value='AdTileHorizontal')

    if not os.path.isdir("media"):
        os.mkdir("media")

    file_name = url.split('/')[-1]
    write_product_json(data=data, file_name=file_name)

    print(f"{file_name} pars completed")

    return data
