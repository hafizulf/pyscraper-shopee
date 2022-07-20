from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)


def get_products(shopee_link):
    driver.set_window_size(1300, 1200)
    driver.get(shopee_link)

    rentang = 500
    for i in range(1, 9):
        akhir = rentang * i
        perintah = 'window.scrollTo(0, ' + str(akhir) + ')'
        driver.execute_script(perintah)
        print('loading ke-' + str(i))
        time.sleep(1)

    time.sleep(5)
    driver.save_screenshot('home.png')
    content = driver.page_source
    driver.quit()

    data = BeautifulSoup(content, 'html.parser')
    # print(data.encode('utf-8'))

    products_url = []

    for area in data.find_all('div', class_='col-xs-2-4 shopee-search-item-result__item'):
        url = area.find('a')['href']

        if url != None:
            complete_url = 'shopee.co.id' + url
            products_url.append(complete_url)

    return products_url
