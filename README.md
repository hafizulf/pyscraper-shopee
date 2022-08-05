# PyScraper

## Description

Pyscraper shopee is a library build with python for web scraping shopee to get some products detail (notebook)

## Prerequisites to Run Application

There are several things that need to be prepared to run this application locally:

### Requires

- <a href="https://www.python.org/">Python<a>
- Download <a href="https://chromedriver.chromium.org/">Chromedriver</a> according to your browser version

### Set Up

- Include chromedrive in the root folder
  - structures

  ```
  ├── docs/
    └── API.md
  ├── src/
    └── producst.py
    └── producsts.py
  app.py
  chromedriver.exe
  README.md
  requirements.txt

  ```

- create and activate local environment

  ```
    python -m venv env
    source ./env/Scripts/activate
  ```

- libraries to install, make sure u already have <a href="https://pypi.org/project/pip/"> pip </a>:

  ```
  pip install -r requirements.txt
  ```

- running application

  ```
  uvicorn app:app --reload
  # custom
  uvicorn --port 5000 --host 127.0.0.1 app:app --reload
  ```

  see API <a href="https://github.com/hafizulf/pyscraper-shopee/blob/main/docs/API.md"> documentation </a>
