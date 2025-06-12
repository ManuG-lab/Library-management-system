from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

# Association Table
book_category = db.Table(
    'book_category',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    bio = db.Column(db.Text, nullable=True)
    birth_date = db.Column(db.Date, nullable=True)

    books = db.relationship('Book', back_populates='author', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'birth_date': self.birth_date
        }


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    books = db.relationship('Book', secondary=book_category, back_populates='categories')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=True)
    membership_date = db.Column(db.Date, nullable=False)

    borrowing_records = db.relationship('Borrowing_record', back_populates='member', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'membership_date': self.membership_date
        }


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.Date, nullable=True)
    isbn = db.Column(db.String(20), nullable=True, unique=True)
    page_count = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    author = db.relationship('Author', back_populates='books')
    categories = db.relationship('Category', secondary=book_category, back_populates='books')
    borrowing_records = db.relationship('Borrowing_record', back_populates='book', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'published_date': self.published_date,
            'isbn': self.isbn,
            'page_count': self.page_count,
            'author_id': self.author_id
        }


class Borrowing_record(db.Model):
    __tablename__ = 'borrowing_record'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=False)

    book = db.relationship('Book', back_populates='borrowing_records')
    member = db.relationship('Member', back_populates='borrowing_records')

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'borrow_date': self.borrow_date,
            'return_date': self.return_date,
            'due_date': self.due_date
        }
