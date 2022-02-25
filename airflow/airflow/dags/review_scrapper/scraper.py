from hashlib import sha1
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

capture_date = datetime.today().strftime("%Y-%m-%d")


example_url = "https://www.goodreads.com/book/show/6088007-neuromancer"

example_book_id = 0

columns = [
    "book_id",
    "date",
    "rating",
    "hash",
    "review_text",
    "capture_date",
]


def get_reviews_from_page(src, book_id):
    page_reviews = set()

    rating_mapping = {
        "did not like it": 1,
        "it was ok": 2,
        "liked it": 3,
        "really liked it": 4,
        "it was amazing": 5,
    }

    date_mapping = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }

    soup = BeautifulSoup(src, "lxml")
    review_elements = soup.find_all("div", {"class": "friendReviews elementListBrown"})

    for review in review_elements:

        try:
            rating = review.find("span", {"class": "staticStars notranslate"})["title"]
            rating = rating_mapping[rating]
        except Exception as e:
            rating = "Null"

        date = review.find("a", {"class": "reviewDate createdAt right"}).text.strip()
        date = date.replace(",", "")
        date = f"{date[-4:]}-{date_mapping[date[:3]]}-{date[4:6]}"
        review_text = review.find("div", {"class": "reviewText stacked"}).text.strip()
        review_text = str(review_text).encode("utf-8")
        page_reviews.add(
            (
                book_id,
                date,
                rating,
                sha1(review_text).hexdigest(),
                review_text.decode("utf-8"),
                capture_date,
            )
        )
    return page_reviews


def get_book_reviews(url, book_id):

    url = url.replace("show", "reviews")

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Accept": "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Referer": f"{url}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "DNT": "1",
        "Sec-GPC": "1",
    }

    querystring = {"sort": "newest", "text_only": "true"}
    payload = ""

    r = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    if r.status_code != 200:
        logging.basicConfig(
            filename="scraper.log",
            level=logging.DEBUG,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info(f"ERROR: status code {r.status_code} and URL: {url}")
        return None

    src = r.content
    src = src.decode("unicode_escape").replace("\n", "")
    src_stripped = src[27:-3]

    page_reviews = get_reviews_from_page(src_stripped, book_id)

    return page_reviews


if __name__ == "__main__":

    page_reviews = get_book_reviews(example_url, example_book_id)

    for review in page_reviews:
        print(review)
