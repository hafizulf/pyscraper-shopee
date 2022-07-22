text_harga = 'Rp3.799.000 - Rp4.799.000'
hargaArray = text_harga.split('-')
harga = int(hargaArray[1].strip().replace('Rp', '').replace('.', ''))
