# Get All Products & Detail

Retrieve all notebook data.

**URL** : `/products?brand=<brand>&max=<price_max>&min=<price_min>&limit=<limit>`

- brand: notebook brand
- max: maximum of product price
- min: minimum of product price
- limit: maximum data you want to get

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**


```json
[
  {
    "url_produk": "https://shopee.co.id/Laptop-Asus-Vivobook-E410MA-L510MA-N4020-4GB-128GB-512GB-Win10-14.0-15.6--i.256652736.9024268861?sp_atk=df51c530-f513-453b-be98-f152d5b4a769&xptdk=df51c530-f513-453b-be98-f152d5b4a769",
    "rating": 4.9,
    "harga": 4999000,
    "merek": "asus",
    "prosesor": "intel celeron",
    "kapasitas_ram": 4,
    "tipe_penyimpanan": "lain",
    "kapasitas_penyimpanan": 512,
    "ukuran_layar": "Portable (13-14,9 inch)",
    "sistem_operasi": "windows",
    "masa_garansi": 12,
    "kondisi_produk": "baru"
  }
]
```
