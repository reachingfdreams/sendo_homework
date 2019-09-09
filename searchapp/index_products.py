from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from searchapp.constants import DOC_TYPE, INDEX_NAME
from searchapp.data import all_products, ProductData


def main():
    # Connect to localhost:9200 by default.
    es = Elasticsearch()

    es.indices.delete(index=INDEX_NAME, ignore=404)
    es.indices.create(
        index=INDEX_NAME,
        body={
            'mappings': {},
            'settings': {},
        },
    )

    # Add all products loaded from json file (simple case) into es.
    # In reality, we can loaded all products from DB or anywhere else.

    # This indexes each product one by one which its not good
    # for performance and take long time if having big data, consider to
    # use bulk index API.
    # for product in all_products():
    #     index_product(es, product)

    # Use bulk indexing API to make index faster.
    bulk(es, products_to_index())

    # See if the indexing job is working or if it has stalled.
    print("Indexed {}".format("all products from json file."))

def products_to_index():
    for product in all_products():
        yield {
            '_op_type': 'index',
            '_index': INDEX_NAME,
            '_type': DOC_TYPE,
            '_id': product.id,
            '_source': {
                'name': product.name,
                'image': product.image,
                'price': product.price,
            },
        }

def index_product(es, product: ProductData):
    """Add a single product to es"""

    es.create(
        index=INDEX_NAME,
        doc_type=DOC_TYPE,
        id=product.id,
        body=product.asDict()
    )


if __name__ == '__main__':
    main()
