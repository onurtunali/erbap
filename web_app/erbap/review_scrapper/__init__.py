"""Scraping reviews and ratings from goodreads.com

DESCRIPTION:

    Scraping the newest reviews from a given goodreads book url. Script works as follows:
        1. Get the given url and open with webdriver of selenium.
        2. Sort the reviews by newest.
        3. Parse the returned web page using BeautifulSoup4 to isolate reviews.
        4. Append the reviews to global mutable list object `reviews`.
        5. Move to the next page until none is left.

DEPENDENCIES:

    - selenium==3.11.0
    - beautifulsoup4==4.10.0
    - geckodriver-v0.30.0-linux64

SCARPING ELEMENTS MAPPING:

    - rating stars `<span class=" staticStars notranslate" title="liked it">`
        - 5: "it was amazing"
        - 4: "really liked it"
        - 3: "liked it"
        - 2: "it was ok"
        - 1: "did not like it"
"""
