HOMEWORK REQUIREMENTS
=====================

Building a simple search engine of product for e-commerce
sites using ElastichSearch with following requirements:

- Create an index with settings and mappings to store products
- Import products (downloaded from https://www.sendo.vn/thoi-trang-nu) into ES
- Write an API to seach product acording to name or description
- Write an API to aggregate the product acording to price

More details, please take a look at homework.pdf

SOLUTIONS
=========

- Using ElastichSearch as search engine

  * Run and start it as a service with local IP and port (default 9200)
  * Create an index with settings and mappings to index products into ES
  * Import the products (json file) into ES
  * Use restFul APIs for indexing and searching

- Deploy a service which provide searching and aggregating APIs
  
  * Using python as http servers
  * Run this server on local IP and port
    (publish IP if deployed to PRODUCTION)
  * Write search API acording name or description, the core logic
    of search of this api uses resful API from ES.
  * Write aggreate API acording to price, the core logic of search
    of this api uses resful API from ES.

TUTORIAL PRE-WORK
=================

To start this homework, first you need to complete the following
prerequisites:

1. Install JDK
   @sudo apt-get install default-jdk@

2. Download, install and run elastich search

	* "Download":https://www.elastic.co/downloads/elasticsearch and
	  unzip the Elasticsearch official distribution.
    You can take directly elastichsearch-6.2.2 from the repository.
	* Run @bin/elasticsearch@
	* Run @curl -X GET http://localhost:9200/@ or open it on browser to check if
    Elastichsearch is working correctly.

3. Insall python, use for simple http server as search app

  * Install python virual env
    @apt-get install python3-venv@

  * In root of the repository, set up a virtualenv:
    @python3 -m venv venv@
    @source venv/bin/activate@

  * Install the necessary python requirements:
    @pip install -r requirements.txt@

  * Set up the searchapp packages.
    @pip install -e .@

START MAIN WORKS
================

1. Create an index with settings and mappings to store products

  We need to understand the RESTFul APIs for creating an index into ES
  and the RESTFul api to add product with the index into ES:

  - RESTFul API to create new index with settings and mappings into ES

    * PUT /index_name
    * The request body
      {
        "settings": {},
        "mappings": {}
      }

  - RESTFul API to add a product with the created index into ES

    * POST /index_name/doc_type/?_create
    * The request body
      {
        ...
      }

  Write the code with pythons using the two above and more APIs:

  - Run @python index_products.py@ to create the index
  - Check the result by opening @http://localhost:9200/sendo/product/1@ on
    the browser

2. Get the all products and import into es

- Write python code to get all products from "https://www.sendo.vn/thoi-trang-nu"

  * Make request to "https://www.sendo.vn/thoi-trang-nu" to take all meta data
    We have useful information from meta data: total_count and total_page
  * Get all products using below API
    GET https://www.sendo.vn/m/wap_v2/category/product?category_id=8&listing_algo=algo5&p=1&platform=web&s=60&sortType=vasup_desc
  * Store all products into json file "thoi-trang-nu.json"
  
- Write python code to import all products fron the json file into es

  * Load all products into ivar, defined in @searchapp/data.py@
  * Logic of importing (indexing) all products from json file written in @searchapp/index_products.py@
