from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re


def get_product_detail(products_url, results_length, limit):

    opsi = webdriver.ChromeOptions()
    opsi.add_argument('--headless')
    servis = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=servis, options=opsi)

    products = []

    if results_length > 0:
        alternatif = results_length
    else:
        alternatif = 0

    # loop all product url
    for url in products_url:

        if alternatif >= limit:
            break

        driver.set_window_size(1300, 1200)
        driver.get(url)

        rentang = 500
        for i in range(1, 5):
            akhir = rentang * i
            perintah = 'window.scrollTo(0, ' + str(akhir) + ')'
            driver.execute_script(perintah)
            print('loading ke-' + str(i))
            time.sleep(1)

        time.sleep(1)
        content = driver.page_source
        data = BeautifulSoup(content, 'html.parser')

        # nama
        try:
            bagian_nama = data.find('div', class_='_2rQP1z')
            nama = bagian_nama.find('span').get_text()
        except:
            nama = 'Unknown'

        # rating produk
        try:
            rating = float(data.find('div', class_='_3y5XOB _14izon').get_text())
        except AttributeError:
            continue

        # harga
        try:
            text_harga = data.find('div', class_='_2Shl1j').get_text()
            hargaArray = text_harga.split('-')
            # check if harga doesn't use range option
            if len(hargaArray) > 1:
                harga = int(hargaArray[1].strip().replace(
                    'Rp', '').replace('.', ''))
            else:
                harga = int(text_harga.strip().replace(
                    'Rp', '').replace('.', ''))
        except AttributeError:
            continue

        # merek
        try:
            merek = data.find('a', class_='_8N1GCt').get_text().lower()
        except AttributeError:
            continue

        # spesifikasi laptop
        subkriteria_list = [
            'prosesor',
            'tipe_penyimpanan',
            'kapasitas_penyimpanan',
            'ukuran_layar',
            'sistem_operasi',
            'garansi',
        ]

        try:
            spesifikasi = data.findAll('div', class_='OktMMO')
        except AttributeError:
            continue

        for subkriteria_tag in spesifikasi:
            try:
                subkriteria = re.search(
                    'class="_27NlLf">(.*)</label>', str(subkriteria_tag)).group(1).lower()
            except AttributeError:
                continue

            # spesifikasi - tipe prosesor
            if subkriteria == 'tipe prosesor':
                prosesor = re.search(
                    '<div>(.*)</div></div>', str(subkriteria_tag)).group(1).lower()
                if(prosesor):
                    subkriteria_list.remove('prosesor')

            # spesifikasi - tipe penyimpanan
            elif subkriteria == 'jenis penyimpanan':
                tipe_penyimpanan = re.search(
                    '<div>(.*)</div></div>', str(subkriteria_tag)).group(1).lower()
                if(tipe_penyimpanan):
                    subkriteria_list.remove('tipe_penyimpanan')

            # spesifikasi - kapasitas penyimpanan
            elif subkriteria == 'kapasitas penyimpanan':
                kapasitas_penyimpanan = re.search(
                    '<div>(.*)</div></div>', str(subkriteria_tag)).group(1).lower()
                if(kapasitas_penyimpanan):
                    subkriteria_list.remove('kapasitas_penyimpanan')

            # spesifikasi - ukuran layar
            elif subkriteria == 'ukuran layar laptop' or subkriteria == 'ukuran layar':
                ukuran_layar = re.search(
                    '<div>(.*)</div></div>', str(subkriteria_tag)).group(1).lower()
                if(ukuran_layar):
                    subkriteria_list.remove('ukuran_layar')

            # spesifikasi - sistem operasi
            elif subkriteria == 'sistem operasi':
                sistem_operasi = re.search(
                    '<div>(.*)</div></div>', str(subkriteria_tag)).group(1).lower()
                if(sistem_operasi):
                    subkriteria_list.remove('sistem_operasi')

            # spesifikasi - masa garansi
            elif subkriteria == 'masa garansi':
                masa_garansi = re.search(
                    '<div>(.*)</div></div>', str(subkriteria_tag)).group(1).lower()
                if(masa_garansi):
                    subkriteria_list.remove('garansi')

            # spesifikasi - kondisi laptop
            elif subkriteria == 'kondisi':
                try:
                    kondisi_produk = re.search(
                        '<div>(.*)</div></div>', str(subkriteria_tag)).group(1).lower()

                    if kondisi_produk != 'baru':
                        kondisi_produk = 'bekas'
                except AttributeError:
                    kondisi_produk = 'bekas'

        # check wether list of subkriteria has been fulfilled
        if(len(subkriteria_list) > 0):
            continue
        else:
            # search in description section
            # kapasitas memory (RAM)
            deskripsi = data.find('p', class_='_2jrvqA').get_text()
            deskripsi_split = deskripsi.splitlines()

            kapasitas_ram = 0
            for line in deskripsi_split:
                line_lower = line.lower()

                if re.findall('ram|memory|memori|ddr|ddr3|ddr4|ddr5', line_lower):
                    line_split = line.split()

                    for index, element in enumerate(line_split):

                        element = element.lower()
                        if re.findall('gb', element):
                            element_split = element.split('gb')

                            try:
                                if int(element_split[0]):
                                    kapasitas_ram = int(element_split[0])
                                    break
                                else:
                                    kapasitas_ram = int(line_split[index - 1])
                                    break
                            except:
                                continue

                    break

            if kapasitas_ram % 2 != 0 or kapasitas_ram == 0:
                continue

            # normalize spesifikasi (sub-kriteria)
            # merek
            merek_list = ['apple', 'asus', 'lenovo', 'hp']
            if merek not in merek_list:
                merek = 'lain'

            # kapasitas penyimpanan
            str_length_kp = len(kapasitas_penyimpanan)
            unit_data = kapasitas_penyimpanan[str_length_kp - 2:]
            if(unit_data == 'gb'):
                kapasitas_penyimpanan = int(
                    kapasitas_penyimpanan.split('gb')[0])
            else:
                kapasitas_penyimpanan = int(
                    kapasitas_penyimpanan.split('tb')[0] + '000')

            # masa garansi
            try:
                garansi = masa_garansi.split(' ')
                str_garansi = garansi[1]

                if str_garansi == 'bulan':
                    garansi = int(garansi[0])
                elif str_garansi == 'minggu':
                    garansi = int(int(garansi[0]) / 4)
                elif str_garansi == 'tahun':
                    garansi = int(int(garansi[0]) * 12)
                else:
                    garansi = 0
            except:
                garansi = 0

            # tipe prosesor
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

            # tipe penyimpanan
            tipe_penyimpanan_list = ['ssd', 'emmc', 'hdd']
            tipe_penyimpanan_split = tipe_penyimpanan.split(' ')
            # check if tipe penyimpanan having more than one, get the first only
            if len(tipe_penyimpanan_split) > 0:
                tipe_penyimpanan = tipe_penyimpanan_split[0].lower()
            if tipe_penyimpanan not in tipe_penyimpanan_list:
                tipe_penyimpanan = 'lain'

            # sistem operasi
            sistem_operasi_list = ['windows', 'linux', 'macos']
            if sistem_operasi not in sistem_operasi_list:
                sistem_operasi = 'lain'

            # ukuran layar
            ukuran_layar = ukuran_layar.split(' ')

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

            if(is_float(ukuran_layar[0])):
                ukuran_layar = number_format(float(ukuran_layar[0]))
            else:
                ukuran_layar = number_format(float(ukuran_layar[1]))

            def get_ukuran_layar(size):
                if(size < 13):
                    return 'Ultra Portable (<13 inch)'
                elif size >= 13 and size <= 14.9:
                    return 'Portable (13-14,9 inch)'
                elif size >= 15 and size <= 16.5:
                    return 'Standard (15-16,5 inch)'
                elif size > 16.5:
                    return 'Large (>16,5 inch)'

            # check some data un-available
            try:
                kondisi_produk
            except:
                kondisi_produk = 'bekas'

        alternatif += 1
        # saving data
        product = {
            'kode': 'A' + str(alternatif),
            'nama': nama,
            'url_produk': url,
            'rating': rating,
            'harga': harga,
            'merk': merek,
            'prosesor': prosesor,
            'kapasitas_ram': kapasitas_ram,
            'tipe_penyimpanan': tipe_penyimpanan,
            'kapasitas_penyimpanan': kapasitas_penyimpanan,
            'ukuran_layar': get_ukuran_layar(ukuran_layar),
            'sistem_operasi': sistem_operasi,
            'masa_garansi': garansi,
            'kondisi_produk': kondisi_produk,
        }

        products.append(product)

    # end of loop
    driver.quit()
    return products
