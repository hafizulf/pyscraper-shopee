# text_harga = 'Rp3.799.000 - Rp4.799.000'
# hargaArray = text_harga.split('-')
# harga = int(hargaArray[1].strip().replace('Rp', '').replace('.', ''))

import re

# <div class="_3Xk7SJ"><label class="UWd0h4">Ukuran Layar Laptop</label><div>14 inci</div></div>
# str = "krunal=21;iwanther19kb"
# result = re.search('krunal=21;(.*)19kb', str)
# print(result.group(1))

str = '<div class="_3Xk7SJ"><label class="UWd0h4">Ukuran Layar Laptop</label><div>14 inci</div></div>'
result = re.search('class="UWd0h4">(.*)</label>', str).group(1)
print(result)
