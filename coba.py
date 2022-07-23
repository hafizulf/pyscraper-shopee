from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

# test satu produk
shopee_link = 'https://shopee.co.id/LAPTOP-MURAH-BARU-LENOVO-IDEAPAD-SLIM-3i-15-N5030-RAM-4GB-512GB-SSD-FHD-WIN11HOME-GREY-i.401207104.10811850777?sp_atk=eb7086b9-9325-4a8d-8380-ae6990619c2e&xptdk=eb7086b9-9325-4a8d-8380-ae6990619c2e'
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


def get_spesifikasi():
    return re.search(
        '<div>(.*)</div></div>', str(subkriteria_tag)).group(1).lower()


# detail product
rating = float(data.find('div', class_='MrYJVA Ga-lTj').get_text())

text_harga = data.find('div', class_='pmmxKx').get_text()
hargaArray = text_harga.split('-')
harga = int(hargaArray[1].strip().replace('Rp', '').replace('.', ''))

merek = data.find('a', class_='kQy1zo').get_text().lower()

spesifikasi = data.findAll('div', class_='_3Xk7SJ')

for subkriteria_tag in spesifikasi:
    subkriteria = re.search(
        'class="UWd0h4">(.*)</label>', str(subkriteria_tag)).group(1).lower()

    if subkriteria == 'tipe prosesor':
        prosesor = get_spesifikasi()
    elif subkriteria == 'jenis penyimpanan':
        tipe_penyimpanan = get_spesifikasi()
    elif subkriteria == 'kapasitas penyimpanan':
        kapasitas_penyimpanan = get_spesifikasi()
    elif subkriteria == 'ukuran layar laptop':
        ukuran_layar = get_spesifikasi()
    elif subkriteria == 'produsen chipset grafis':
        kartu_grafis = get_spesifikasi()
    elif subkriteria == 'sistem operasi':
        sistem_operasi = get_spesifikasi()
    elif subkriteria == 'masa garansi':
        masa_garansi = get_spesifikasi()
    elif subkriteria == 'kondisi':
        kondisi_produk = get_spesifikasi()

# Search for Memory (RAM)
bagian_varian = data.find_all('label', class_='_0b8hHE')

varians = []
for elemen in bagian_varian:
    label_text = elemen.get_text().lower()
    varians.append(label_text)

if 'variann' and 'varian' in varians:
    kapasitas_ram = False
else:
    for varian in bagian_varian:
        vLabel = varian.get_text().lower()

        if vLabel == 'varian' or vLabel == 'storage':
            sibling = varian.next_sibling
            varian_pertama = sibling.find(
                'button', class_='product-variation').get_text()
            kapasitas_ram = int(varian_pertama.split('/')[0])

detail_product = {
    'rating': rating,
    'harga': harga,
    'merek': merek,
    'prosesor': prosesor,
    'kapasitas_ram': kapasitas_ram,
    'tipe_penyimpanan': tipe_penyimpanan,
    'kapasitas_penyimpanan': kapasitas_penyimpanan,
    'ukuran_layar': ukuran_layar,
    'kartu_grafis': kartu_grafis,
    'sistem_operasi': sistem_operasi,
    'masa_garansi': masa_garansi,
    'kondisi_produk': kondisi_produk,
}

print(detail_product)
