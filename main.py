import helper
import detail

shopee_link = 'https://shopee.co.id/search?keyword=laptop'
products_url = helper.get_products(shopee_link)

products = detail.get_product_detail(products_url)
print(products)
