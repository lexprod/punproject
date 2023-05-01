"""
Populate punproj database with fake data using the SQLAlchemy ORM.
"""

import random
import string
import hashlib
import secrets
from faker import Faker
from punproj.src.models import User, Pun, Category, puns_categories_table, db
from punproj.src import create_app

USER_COUNT = 50
PUN_COUNT = 50
CATEGORY_COUNT = 50

import random

def truncate_tables():
    """Delete all rows from database tables"""
    db.session.execute(puns_categories_table.delete())
    User.query.delete()
    Pun.query.delete()
    Category.query.delete()
    db.session.commit()


def generate_username():
    faker = Faker()
    while True:
        user_name = faker.first_name() + secrets.randbelow(1000).__str__().zfill(3)
        return user_name


def main():
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    #first create random users
    for i in range(USER_COUNT):
        random_username = generate_username()
        dummy_pw = 'password123!'
        user = User(user_name=random_username, password=dummy_pw)
        db.session.add(user)
    # commit all changes to the database so theres users to reference when puns are built
    db.session.commit()

    # create  random puns with random text and user ID 
    # make list of users to use
    user_ids = [user.id for user in User.query.all()]
    for i in range(PUN_COUNT):
        pun_text= fake.text(max_nb_chars=100)
        user_id = random.choice(user_ids)
        pun = Pun(pun_text=pun_text, user_id=user_id)
        db.session.add(pun)
    # commit all puns
    db.session.commit()

    for i in range(CATEGORY_COUNT):
        category_name = fake.word()
        category = Category(category_name=category_name)
        db.session.add(category)
    db.session.commit()

# run script
main()
