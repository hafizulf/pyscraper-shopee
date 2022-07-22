from ast import If
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

# test satu produk
shopee_link = 'https://shopee.co.id/LAPTOP-SLIM-DESIGN-ASUS-VIVOBOOK-E410MA-INTEL-N4020-RAM-4GB-512GB-SSD-WIN10-HOME-i.401207104.9824331654?sp_atk=0562838e-f4dc-4e48-a945-76c1d553fbb5&xptdk=0562838e-f4dc-4e48-a945-76c1d553fbb5'
driver.set_window_size(1300, 1200)
driver.get(shopee_link)

rentang = 500
for i in range(1, 5):
    akhir = rentang * i
    perintah = 'window.scrollTo(0, ' + str(akhir) + ')'
    driver.execute_script(perintah)
    print('loading ke-' + str(i))
    time.sleep(1)

time.sleep(5)
driver.save_screenshot('product.png')
content = driver.page_source
driver.quit()

data = BeautifulSoup(content, 'html.parser')

# detail product
rating = float(data.find('div', class_='MrYJVA Ga-lTj').get_text())

text_harga = data.find('div', class_='pmmxKx').get_text()
hargaArray = text_harga.split('-')
harga = int(hargaArray[1].strip().replace('Rp', '').replace('.', ''))

merek = data.find('a', class_='kQy1zo').get_text().lower()

spesifikasi = data.findAll('div', class_='_3Xk7SJ')

for subkriteria in spesifikasi:
    print(subkriteria)
    # check by label => class_='UWd0h4'
    # elemen = label.get_text().lower()

    # if elemen == 'ukuran layar laptop':
    #     ukuran_layar = elemen
    # elif elemen == 'tipe prosesor':
    #     prosesor = elemen

detail_product = {
    'rating': rating,
    'harga': harga,
    'merek': merek,
}

print(detail_product)
