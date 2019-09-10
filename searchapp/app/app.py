from flask import Flask, render_template, request

from searchapp.data import all_products
from searchapp.app.search import search, search_for_price_range

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        products_by_category=[],
    )


@app.route('/search', methods=['GET', 'POST'])
def search_single_product():
    """
    Execute a search for a specific search term.

    Return the top 60 results.
    """
    num_results = 60
    products_by_category = []

    name_or_description = request.args.get('search')
    if name_or_description != None:
        products_by_category = [(name_or_description, search(name_or_description, num_results))]
    elif request.args.get('min_price') != None or request.args.get('max_price') != None:
        min_price = request.args.get('min_price')
        if min_price == None or min_price.isdigit() == False:
            min_price = 0
        max_price = request.args.get('max_price')
        if max_price == None or max_price.isdigit() == False:
            max_price = 0
        products_by_category = [("Price in [{}, {}] VND".format(min_price, max_price),
                                search_for_price_range(min_price, max_price, num_results))]

    return render_template(
        'index.html',
        products_by_category=products_by_category
    )


@app.route('/product/<int:product_id>')
def single_product(product_id):
    """
    Display information about a specific product
    """

    product = str(all_products()[product_id - 1])

    return render_template(
        'product.html',
        product_json=product,
        search_term='',
    )
