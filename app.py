from fastapi import FastAPI
import time

import src.products as products
import src.product as product

app = FastAPI()


@app.get("/products")
def get_products(brand: str = 'laptop', max: int = 0, min: int = 0,  limit: int = 20):
    results = []

    page_number = 0
    while len(results) < limit:
        link = f'https://shopee.co.id/search?keyword={brand}&maxPrice={max}&minPrice={min}&page={page_number}'
        urls = products.get_products_url(link)

        time.sleep(2)

        results_length = len(results)
        result = product.get_product_detail(urls, results_length, limit)
        results.extend(result)

        page_number += 1

    return results
