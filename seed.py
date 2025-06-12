from faker import Faker
import random
from datetime import timedelta
from models import db, Author, Book, Category, Member, Borrowing_record
from datetime import date
from app import app
from flask_migrate import Migrate
fake = Faker()


def seed_authors(num_authors=20):
    for _ in range(num_authors):
        author = Author(
            name=fake.name(),
            email=fake.email(),
            bio=fake.text(max_nb_chars=200),
            birth_date=fake.date_of_birth(minimum_age=20, maximum_age=80)
        )
        db.session.add(author)
    db.session.commit()

def seed_books(num_books=50):
    authors = Author.query.all()
    for _ in range(num_books):
        book = Book(
            title=fake.sentence(nb_words=3),
            published_date=fake.date_between(start_date='-10y', end_date='today'),
            isbn=fake.isbn13(),
            page_count=fake.random_int(min=100, max=1000),
            author_id=fake.random_element(authors).id
        )
        db.session.add(book)
    db.session.commit()

def seed_categories():
    print("Seeding categories...")
    db.session.query(Category).delete()

    unique_names = set()
    categories = []

    while len(unique_names) < 10:
        name = fake.word()
        if name not in unique_names:
            unique_names.add(name)
            category = Category(
                name=name,
                description=fake.text()
            )
            categories.append(category)

    db.session.add_all(categories)
    db.session.commit()


def seed_members(num_members=100):
    for _ in range(num_members):
        member = Member(
            name=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            membership_date=fake.date_between(start_date='-5y', end_date='today')
        )
        db.session.add(member)
    db.session.commit()

def seed_borrowing_records():
    print("Seeding borrowing records...")
    books = Book.query.all()
    members = Member.query.all()

    for _ in range(50):
        book = random.choice(books)
        member = random.choice(members)
        borrow_date = fake.date_between(start_date='-6M', end_date='today')
        due_date = borrow_date + timedelta(days=14)  # 2 weeks due date

        # 50% chance the book was returned
        return_date = None
        if random.choice([True, False]):
            return_date = fake.date_between(start_date=borrow_date, end_date=borrow_date + timedelta(days=30))

        record = Borrowing_record(
            book_id=book.id,
            member_id=member.id,
            borrow_date=borrow_date,
            due_date=due_date,
            return_date=return_date
        )
        db.session.add(record)

    db.session.commit()

def run_seed():
    with app.app_context():
        print("Seeding authors...")
        seed_authors()
        print("Seeding categories...")
        seed_categories()
        print("Seeding books...")
        seed_books()
        print("Seeding members...")
        seed_members()
        print("Seeding borrowing records...")
        seed_borrowing_records()
        print("✅ Database seeded successfully!")

if __name__ == '__main__':
    run_seed()
                     