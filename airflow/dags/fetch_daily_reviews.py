import os
from datetime import datetime, timedelta
from urllib.parse import urlparse

from airflow import DAG
from airflow.operators.python import PythonOperator
from mysql.connector import Error, connect
from review_scrapper import scraper


current_date = datetime.today().strftime("%Y-%m-%d")

DATABASE_URI = os.getenv("AIRFLOW_CONN_MYSQL_DEFAULT")

dbc = urlparse(DATABASE_URI)

# Default settings applied to all tasks
default_args = {
    "owner": "onur tunali",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


dag = DAG(
    dag_id="fetch_all_reviews",
    start_date=datetime.today() - timedelta(days=1),
    schedule_interval="0 0 * * *",
    default_args=default_args,
)


def get_urls():

    try:
        with connect(
            host=dbc.hostname,
            user=dbc.username,
            password=dbc.password,
            database=dbc.path.lstrip("/"),
        ) as connection:
            cursor = connection.cursor()
            query = """
            SELECT DISTINCT B.id, url 
            FROM books AS B left join reviews AS R on R.book_id = B.id
            WHERE R.capture_date is NULL or R.capture_date <> %s
            """
            cursor.execute(query, params=(current_date,))
            urls = cursor.fetchall()  # result is a tuple

    except Error as e:
        print(e)

    return urls


def insert_reviews(urls):

    insert_query = (
        """INSERT IGNORE INTO reviews VALUES (Null, %s, %s, %s, %s, %s, %s)"""
    )
    for url in urls[:2]:  # for test
        reviews = scraper.get_book_reviews(url[1], url[0])
        reviews = list(reviews)  # params requires a list
        try:
            with connect(
                host=dbc.hostname,
                user=dbc.username,
                password=dbc.password,
                database=dbc.path.lstrip("/"),
            ) as connection:
                cursor = connection.cursor()
                cursor.executemany(insert_query, params=reviews)
                cursor.execute(
                    "UPDATE reviews set capture_date = %s where book_id = %s",
                    (current_date, reviews[0][0]),
                )
                connection.commit()

        except Error as e:
            print(e)


urls = get_urls()

get_reviews = PythonOperator(
    task_id="fetch_reviews", python_callable=insert_reviews, op_args=urls, dag=dag
)
