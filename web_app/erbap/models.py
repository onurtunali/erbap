from erbap import db
from flask import current_app


class Book(db.Model):

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(200))
    author_name = db.Column(db.String(200))
    edition_language = db.Column(db.String(8))
    rating_score = db.Column(db.Float)
    rating_votes = db.Column(db.Integer)
    review_number = db.Column(db.Integer)
    book_description = db.Column(db.Text())
    year_published = db.Column(db.Integer)
    genres = db.Column(db.Text())
    url = db.Column(db.String(200))
    cover = db.Column(db.String(200))
    # reviews = db.relationship("Review", backref="author", lazy=True)

    def __repr__(self):
        return f"Book('{self.book_title}', '{self.author_name}', '{self.rating_score}')"


class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    date = db.Column(db.Date)
    rating = db.Column(db.Float)
    hash = db.Column(db.String(50), unique=True, nullable=False)
    review_text = db.Column(db.Text())
    capture_date = db.Column(db.Date)

    def __repr__(self):
        return f"Review('{self.book_id}', '{self.date}', '{self.rating}')"
