from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time


def get_products_url(shopee_link):
    opsi = webdriver.ChromeOptions()
    opsi.add_argument('--headless')
    servis = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=servis, options=opsi)

    driver.set_window_size(1300, 1200)
    driver.get(shopee_link)

    rentang = 500
    for i in range(1, 9):
        akhir = rentang * i
        perintah = 'window.scrollTo(0, ' + str(akhir) + ')'
        driver.execute_script(perintah)
        print('loading ke-' + str(i))
        time.sleep(1)

    time.sleep(3)

    content = driver.page_source
    driver.quit()

    data = BeautifulSoup(content, 'html.parser')

    products_url = []

    for area in data.find_all('div', class_='col-xs-2-4 shopee-search-item-result__item'):
        try:
            url = area.find('a')['href']
        except TypeError:
            continue

        if url != None:
            complete_url = 'https://shopee.co.id' + url
            products_url.append(complete_url)

    return products_url
