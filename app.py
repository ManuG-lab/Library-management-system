from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date
from models import db, Author, Book, Category, Member, Borrowing_record

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

#------------------- HOME -------------------#
@app.route('/')
def home():
    return {'message': 'Welcome to the Library API'}

#------------------- AUTHORS -------------------#
@app.route('/authors', methods=['GET'])
def get_authors():
    return jsonify([author.to_dict() for author in Author.query.all()])

@app.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = Author.query.get_or_404(author_id)
    return jsonify(author.to_dict())

@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    new_author = Author(
        name=data['name'],
        email=data['email'],
        bio=data.get('bio'),
        birth_date=data.get('birth_date')
    )
    db.session.add(new_author)
    db.session.commit()
    return jsonify(new_author.to_dict()), 201

#------------------- BOOKS -------------------#
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify([book.to_dict() for book in Book.query.all()])

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        published_date=data.get('published_date'),
        isbn=data.get('isbn'),
        page_count=data.get('page_count'),
        author_id=data['author_id']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

#------------------- CATEGORIES -------------------#
@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify([category.to_dict() for category in Category.query.all()])

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict())

@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

#------------------- MEMBERS -------------------#
@app.route('/members', methods=['GET'])
def get_members():
    return jsonify([member.to_dict() for member in Member.query.all()])

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = Member.query.get_or_404(member_id)
    return jsonify(member.to_dict())

@app.route('/members', methods=['POST'])
def create_member():
    data = request.get_json()
    new_member = Member(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        address=data.get('address')
    )
    db.session.add(new_member)
    db.session.commit()
    return jsonify(new_member.to_dict()), 201

#------------------- BORROWING RECORDS -------------------#
@app.route('/borrowing_records', methods=['GET'])
def get_borrowing_records():
    return jsonify([record.to_dict() for record in Borrowing_record.query.all()])

@app.route('/borrowing_records/<int:record_id>', methods=['GET'])
def get_borrowing_record(record_id):
    record = Borrowing_record.query.get_or_404(record_id)
    return jsonify(record.to_dict())

@app.route('/borrowing_records', methods=['POST'])
def create_borrowing_record():
    data = request.get_json()
    new_record = Borrowing_record(
        book_id=data['book_id'],
        member_id=data['member_id'],
        borrow_date=data.get('borrow_date', date.today()),
        return_date=data.get('return_date'),
        due_date=data.get('due_date')
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.to_dict()), 201

#------------------- ERROR HANDLER -------------------#
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

#------------------- RUN APP -------------------#
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
