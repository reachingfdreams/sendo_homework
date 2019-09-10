from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from typing import List

from searchapp.constants import DOC_TYPE, INDEX_NAME

HEADERS = {'content-type': 'application/json'}


class SearchResult():
    """Represents a product returned from elasticsearch."""
    def __init__(self, id_, image, name):
        self.id = id_
        self.image = image
        self.name = name

    def from_doc(doc) -> 'SearchResult':
        return SearchResult(
                id_ = doc.meta.id,
                image = doc.image,
                name = doc.name,
            )


def search(term: str, count: int) -> List[SearchResult]:
    client = Elasticsearch()

    # Elasticsearch 6 requires the content-type header to be set, and this is
    # not included by default in the current version of elasticsearch-py
    client.transport.connection_pool.connection.headers.update(HEADERS)

    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE)
    description_query = {
        'match': {
            'description': {
                'query': term,
                'operator': 'and',
                'fuzziness': 'AUTO',
            }
        }
    }
    name_query = {
        'match': {
            'name': {
                'query': term,
                'operator': 'and',
                'fuzziness': 'AUTO',
            }
        }
    }
    dismax_query = {
        'dis_max': {
            'queries': [name_query, description_query],
        },
    }
    docs = s.query(dismax_query)[:count].execute()

    return [SearchResult.from_doc(d) for d in docs]

def search_for_price_range(min_price: int, max_price: int, count: int) -> List[SearchResult]:
    """ Search all products acording to price range. """

    client = Elasticsearch()

    # Elasticsearch 6 requires the content-type header to be set, and this is
    # not included by default in the current version of elasticsearch-py
    client.transport.connection_pool.connection.headers.update(HEADERS)

    # TODO: seperate three cases, [min_price, ], [, max_price],
    # and [min_price, max_price].
    body = {
        "query": {
            "range": {
                "price": {
                    "gte": min_price,
                    "lte": max_price
                }
            }
        }
    }
    s = Search(using=client, index=INDEX_NAME, doc_type=DOC_TYPE).update_from_dict(body)
    docs = s.query()[:count].execute()

    return [SearchResult.from_doc(d) for d in docs]
