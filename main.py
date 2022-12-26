from multiprocessing import Pool

from parser_app import category, product

URL = 'https://lalafo.kg/sitemap'


def main():
    category_links = category.get_category_links(url=URL)
    links = [i['link'] for i in category_links]
    processes = int(input('Enter amount of process: '))
    p = Pool(processes=processes)
    p.map(product.get_product_data, links)


if __name__ == '__main__':
    main()
