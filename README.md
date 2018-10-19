# Store-Manager

[![Build Status](https://travis-ci.org/BarnaTB/Store-Manager.svg?branch=ft-api)](https://travis-ci.org/BarnaTB/Store-Manager) [![Coverage Status](https://coveralls.io/repos/github/BarnaTB/Store-Manager/badge.svg?branch=ft-api)](https://coveralls.io/github/BarnaTB/Store-Manager?branch=ft-api) [![codecov](https://codecov.io/gh/BarnaTB/Store-Manager/branch/ft-api/graph/badge.svg)](https://codecov.io/gh/BarnaTB/Store-Manager) [![Maintainability](https://api.codeclimate.com/v1/badges/2a139d2008a480d3f1c9/maintainability)](https://codeclimate.com/github/BarnaTB/Store-Manager/maintainability) [![Build status](https://ci.appveyor.com/api/projects/status/jiis6u165xnh0xq6/branch/ft-api?svg=true)](https://ci.appveyor.com/project/BarnaTB/store-manager/branch/ft-api)


This is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.

## Getting Started

You can clone the project using the link [Github repository](https://github.com/BarnaTB/Store-Manager.git).

## Prerequisites

The UI pages do not need much to be viewed as any web browser can view them from [this site](https://barnatb.github.io/Store-Manager/) as long as they have internet access. Please note that the UI is static at the moment as work is underway to connect the back-end to it.

## Installing

* Clone the project into your local repository using this command:

```sh
  $ git clone https://github.com/BarnaTB/Store-Manager.git
  ```
  Switch to the cloned directory, install a virtual environment, create a virtual environment, activate it, checkout to the most stable branch, install app dependencies and run the app.
  ```sh
    $ cd Store-Manager
    $ pip install virtualenv
    $ virtualenv venv
    $ source venv/bin/activate
    $ git checkout ft-api
    $ pip install -r requirements.txt
    $ python3 run.py
```
**Note** If you're using Windows, activate your virtualenv using `` $ source venv/Scripts/activate ``
* Copy the url http://127.0.0.1:5000/ into your Postman and to run any endpoint follow the table under the heading (**Endpoints**) with the url prefix ('/api/v1') for each endpoint.

## Endpoints
HTTP Method | Endpoint | Functionality | Parameters | Protected
----------- | -------- | ------------- | ---------- | ---------
POST | /products | Create a product | None | False
GET | /products/int:product_id | Fetch a single product record | product_id | False
GET | /products | Fetch all products | None | False
POST | /sales | Create a sale order | None | False
GET | /sales/sale_id | Fetch a single sale record | sale_id | False
GET | /sales | Fetch all sale records | None | False

## Running the tests

Install pytest, source the .env file, run the tests.
```sh
  $ pip install pytest
  $ python3 -m pytest
  ```

## Deployment


## Tools Used

* [Flask](http://flask.pocoo.org/) - Web microframework for Python
* [Virtual environment](https://virtualenv.pypa.io/en/stable/) - tool used to create isolated python environments
* [pip](https://pip.pypa.io/en/stable/) - package installer for Python

## Built With

The project has been built with the following technologies so far:

* HTML
* CSS
* Javascript
* Python/Flask

## Contributions

To contibute to the project, create a branch from the **develop** branch and make a PR after which your contributions may be merged into the **develop** branch

## Authors

Barnabas Tumuhairwe B
