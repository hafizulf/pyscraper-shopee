import time

import products
import product

shopee_link = 'https://shopee.co.id/search?keyword=laptop'
products_url = products.get_products_url(shopee_link)

time.sleep(5)

result = product.get_product_detail(products_url)
print(result)
