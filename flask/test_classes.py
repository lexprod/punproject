from punproj.src.models import User, Pun, Category, puns_categories_table, ratings_table, db
from punproj.src import create_app


def test_user_init():
    u1 = User('user', 'pw1')
    assert u1.user_name == 'user'
    assert u1.password == 'pw1'

def test_pun_init():
    p1 = Pun('pun', 1234)
    assert p1.pun_text == 'pun'
    assert p1.user_id == 1234

def test_category_init():
    c1 = Category('category')
    assert c1.category_name == 'category'
