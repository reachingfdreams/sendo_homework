from elasticsearch import Elasticsearch

from searchapp.constants import DOC_TYPE, INDEX_NAME


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

    index_testing_product(es)


def index_testing_product(es):
    """Add a single product to es for testing"""

    es.create(
        index=INDEX_NAME,
        doc_type=DOC_TYPE,
        id=1,
        body={
            "name": "Testing Product",
            "image": "http://sendo.vn/thoi-trang-nu/ao-len.png",
        }
    )

    # See if the indexing job is working or if it has stalled.
    print("Indexed {}".format("Testing Product"))


if __name__ == '__main__':
    main()
