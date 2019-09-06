HOMEWORK REQUIREMENTS
=====================

Building a simple search engine of product for e-commerce
sites using ElastichSearch with following requirements:

- Import products (downloaded from https://www.sendo.vn/thoi-trang-nu) into ES
- Write an API to seach product acording to name or description
- Write an API to aggregate the product acording to price

More details, please take a look at homework.pdf

SOLUTIONS
=========

- Using ElastichSearch as search engine

  * Run and start it as a service with local IP and port.
  * Create mapping to index products into ES
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
	* Run @bin/elasticsearch@
	* Run @curl -X GET http://localhost:9200/@ or open it on browser.

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
