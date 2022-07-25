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
# driver.save_screenshot('product.png')
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
        v_label = varian.get_text().lower()

        if v_label == 'varian' or v_label == 'storage':
            sibling = varian.next_sibling
            varian_pertama = sibling.find(
                'button', class_='product-variation').get_text()
            kapasitas_ram = int(varian_pertama.split('/')[0])

# normalize
kapasitas_penyimpanan = int(kapasitas_penyimpanan.split('gb')[0])

garansi = masa_garansi.split(' ')
if garansi[1] == 'bulan':
    garansi = int(garansi[0])
else:
    garansi = 0

prosesor_list = [
    'intel core i7',
    'amd ryzen 5',
    'intel core i5',
    'amd ryzen 3',
    'intel core i3',
    'intel celeron',
]
if prosesor not in prosesor_list:
    prosesor = 'lain'

tipe_penyimpanan_list = [
    'ssd',
    'emmc',
    'hdd',
]
if tipe_penyimpanan not in tipe_penyimpanan_list:
    tipe_penyimpanan = 'lain'

kartu_grafis_list = [
    'nvidia geforce',
    'amd radeon',
    'intel hd',
    'intel uhd',
]
if kartu_grafis not in kartu_grafis_list:
    kartu_grafis = 'lain'

sistem_operasi_list = [
    'windows',
    'linux',
    'macos'
]
if sistem_operasi not in sistem_operasi_list:
    sistem_operasi = 'lain'

if kondisi_produk != 'baru':
    kondisi_produk = 'bekas'

# Ukuran Layar


def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False


def number_format(num):
    if num % 1 == 0:
        return int(num)
    else:
        return float(num)


ukuran_layar = ukuran_layar.split(' ')

if(is_float(ukuran_layar[0])):
    ukuran_layar = number_format(float(ukuran_layar[0]))
else:
    ukuran_layar = number_format(float(ukuran_layar[1]))


def get_ukuran_layar(size):
    if(size < 13):
        return 'Ultra Portable (< 13 inch)'
    elif size >= 13 and size <= 14.9:
        return 'Portable (13-14,9 inch)'
    elif size >= 15 and size <= 16.5:
        return 'Standard (15-16.5 inch)'
    elif size > 16.5:
        return 'Large (> 16.5 inch)'


# save data
detail_product = {
    'rating': rating,
    'harga': harga,
    'merek': merek,
    'prosesor': prosesor,
    'kapasitas_ram': kapasitas_ram,
    'tipe_penyimpanan': tipe_penyimpanan,
    'kapasitas_penyimpanan': kapasitas_penyimpanan,
    'ukuran_layar': get_ukuran_layar(ukuran_layar),
    'kartu_grafis': kartu_grafis,
    'sistem_operasi': sistem_operasi,
    'masa_garansi': garansi,
    'kondisi_produk': kondisi_produk,
}

print(detail_product)
