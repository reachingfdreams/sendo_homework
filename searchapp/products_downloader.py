import json
import os
import sys
import urllib3

def url_to_fetch(page_index: int):
    return 'https://www.sendo.vn/m/wap_v2/category/product?category_id=8&listing_algo=algo5&p={}&platform=web&s=60&sortType=vasup_desc'.format(page_index)

def fetch_products_metadata():
    """
    Fetches products meta data from SENDO thoi-trang-nu catogory

    Returns the dictionary of toltal_count and total_page.
    """
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    r = http.request('GET', url_to_fetch(1))
    if r.status == 200:
        try:
            meta_data = json.loads(r.data.decode('utf8'))['result']['meta_data']
            print("Fetch products meta data successfully\ntotal_count=%d, total_page=%d\n"
                % (meta_data['total_count'], meta_data['total_page']))
            return meta_data
        except:
            print("Fetch successfully, but cannot parse meta data, data struct changed.")
            return {}
    else:
        print('Network unavailable or server down to fetch meta data.')
        return {}

def fetch_products_for(page_index: int):
    """
    Fetches all products of specific page idnex |page_int|.

    Returns the list of products.
    """
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    r = http.request('GET', url_to_fetch(page_index))

    if r.status == 200:
        try:
            products_data = json.loads(r.data.decode('utf8')
                                )['result']['data']
            shorted_products = []
            for product in products_data:
                try:
                    shorted_products.append("{\"name\": \"%s\", \"image\": \"%s\", \"price\": %d}"
                                            % (product['name'], product['image'], product['price']))
                except:
                    continue;
            print("Fetch {} products for page No. {}"
                .format(len(shorted_products), page_index))
            return shorted_products
        except:
            print("Cannot parse products for page No. {}"
                .format(page_index))
            return []
    else:
        print('Network unavailable or server down to fetch products for page No. {}'
            .format(page_index))
        return []

def fetch_all_products(max_pages_to_fetch: int):
    """
    Makes requests to SENDO to take all the products of
    the catogory "thoi-trang-nu": https://sendo.vn/thoi-trang-nu

    All products after fetchin will be written into products.json.
    """

    # Remove the products.json before start fetching data fron SENDO.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    products_path = os.path.join(dir_path, 'products.json')
    if os.path.isfile(products_path):
        os.remove(products_path)

    # Fetch meta data and fetch all products.
    # This logic now fetches products from the page index
    # one by one synchronously that may take mins even more to
    # complete a big data.
    # An ivar to store all products in in-memory(RAM)
    # TODO: Implement better solution for it. 
    meta_data = fetch_products_metadata()
    if meta_data['total_page'] == 0 or meta_data['total_count'] == 0:
        print("There's no product availbles to fetch.")
    else:
        all_products = []
        for i in range(0, min(meta_data['total_page'], max_pages_to_fetch), 1):
            products = fetch_products_for(i + 1)
            if len(products) != 0:
                all_products.extend(products)
                
        f = open(products_path, "w+")
        f.write("[\n")
        product_index = 0
        for product in all_products:
            if product_index != 0:
                f.write(",")
                f.write("\n")
            product_index += 1
            f.write(" {}".format(product))
        f.write("\n]")

if __name__ == '__main__':
    page_number_to_fetch = 100
    cmd_args_len = len(sys.argv)
    if cmd_args_len == 2:
        if sys.argv[1].isdigit():
            page_number_to_fetch = int(sys.argv[1])
    print("Start fetching 60 x {} products\n".format(page_number_to_fetch))
    fetch_all_products(page_number_to_fetch)
