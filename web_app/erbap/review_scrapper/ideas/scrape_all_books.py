import time
from hashlib import sha1
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from random import randint
from concurrent.futures import ThreadPoolExecutor

df = pd.read_csv("data/scifi_with_cover.csv")

scraping_status = [True] * df.shape[0]

logging.basicConfig(
    filename="scraper.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
)

reviews = []
URL_PARAMETERS = "?sort=newest&text_only=true"
urls = df.url.values
book_ids = df.id.values

columns = [
    "book_id",
    "date",
    "rating",
    "hash",
    "review_text",
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
            rating = review.find("span", {"class": " staticStars notranslate"})["title"]
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
            )
        )
    return page_reviews


def main(url, book_id):
    url = url.replace("show", "reviews")

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Accept": "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Related-Request-Id": "FN56H1B7J0DAFGDBZ1BQ",
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

    if r.status_code == 200:
        time.sleep(randint(3, 10))
    else:
        time.sleep(20)
        print(r.status_code)
        return []

    src = r.content
    src = src.decode("unicode_escape").replace("\n", "")
    src_stripped = src[27:-3]
    page_reviews = get_reviews_from_page(src_stripped, book_id)

    try:
        latest_date = sorted(page_reviews, key=lambda x: x[1], reverse=True)[0][1]
    except:
        logging.info(f"NO DATE ==== Book id: {book_id} and url {url}")

    print(f"Book id: {book_id} # of reviews: {len(page_reviews)}")
    return page_reviews


with ThreadPoolExecutor(max_workers=5) as executor:

    for future in executor.map(
        lambda args: main(*args), zip(urls[100:150], book_ids[100:150])
    ):
        reviews.extend(future)

reviews_df = pd.DataFrame(reviews)
reviews_df.columns = columns
reviews_df.to_csv("reviews.csv", index=False)
