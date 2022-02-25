from flask import render_template, request, Blueprint
from erbap import db
from sqlalchemy import text
from random import randint


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/random")
def random():
    """API endpoint for generating random books for `index.html`."""

    number_of_books = 5
    # TODO: 9847 is number of books and hardcoded, needs to be changes
    random_indexes = tuple([randint(1, 9847) for _ in range(number_of_books)])

    # TODO: func.rand() is MySQL specific, needs to be changed
    query = text(f"SELECT * FROM books WHERE id IN {random_indexes}")
    with db.session() as session:
        books = session.execute(query)
    return render_template("random.html", books=books)


@main.route("/search", methods=("GET", "POST"))
def search():
    if request.method == "POST":
        title = request.form["search"]

    with db.session() as session:
        query = text(f"SELECT * FROM books WHERE book_title LIKE '%{title}%' LIMIT 10")

        books = session.execute(query).fetchall()
    return render_template("results.html", books=books)
