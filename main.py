from parser_app import category, product

URL = 'https://lalafo.kg/sitemap'


def main():
    category_links = category.get_category_links(url=URL)
    category.write_json(data=category_links)
    for category_link in category_links:
        product_data = product.get_product_data(category_link['link'])
        product.write_product_json(product_data, category_link['title'])


if __name__ == '__main__':
    main()
