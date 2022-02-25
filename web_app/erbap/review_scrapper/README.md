# Web Scraping 

Goodreads review section uses AJAX principles to update reviews without fetching new html page. For this reason we are not able to scrap web pages without using a headless browser to interact with interactive elements.

```bash
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
$ tar xvfz geckodriver-v0.19.1-linux64.tar.gz
$ mv geckodriver ~/.local/bin
```

