from flask import Blueprint
from flask import jsonify
from flask import abort, request
from ..models import Pun, User, db, ratings_table, Category, puns_categories_table
from flask import current_app as app
from sqlalchemy import func

bp = Blueprint('puns', __name__, url_prefix='/puns')

@bp.route('', methods=['GET'])
def index():
    puns = Pun.query.all()
    results = []
    for p in puns:
        results.append(p.serialize())

    return jsonify(results)


@bp.route('/<int:pun_id>', methods=['GET', 'DELETE'])
def show_or_delete(pun_id: int):
    if request.method == 'GET':
        p = Pun.query.get(pun_id)
        return jsonify(p.serialize())
    elif request.method == 'DELETE':
        p = Pun.query.get_or_404(pun_id)
        try:
            db.session.delete(p)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)
        
@bp.route('/<int:pun_id>/avg', methods=['GET'])
def pun_avg_rating(pun_id):
    pun = Pun.query.get(pun_id)

    if not pun:
        return jsonify({'error': 'Pun not found'}), 404
    
    avg_rating = db.session.query(func.avg(ratings_table.c.rating)).filter_by(pun_id=pun_id).scalar()
    return jsonify({'average_rating': str(avg_rating)})
    

#add or update rating to pun
@bp.route('/<int:pun_id>/rate', methods=['POST', 'PUT', 'PATCH'])
def rate_pun(pun_id):
    pun = Pun.query.get(pun_id)
    data = request.get_json()
    rating = data.get('rating')
    user_id = data.get('user_id')
    user = User.query.get(user_id)

    # Make sure the user and pun exist

    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not pun:
        return jsonify({'error': 'Pun not found'}), 404
    
    # check that rating is 1-5
    if not (1 <= int(rating) <=5 ):
        return jsonify({'error': 'Invalid rating.'}), 404
        
    # check if the user has already rated the pun
    existing_rating = db.session.query(ratings_table).filter_by(user_id=user.id, pun_id=pun.id).first()
    if existing_rating:
        # update the existing rating
        update = ratings_table.update().where(ratings_table.c.user_id == user.id).where(ratings_table.c.pun_id == pun.id).values(rating=rating)
        db.session.execute(update)
    else:
        # create a new rating
        new_rating = ratings_table.insert().values(pun_id=pun_id, user_id=user.id, rating=rating)
        db.session.execute(new_rating)
    
    db.session.commit()

    return jsonify({'message': 'Rating submitted'})


@bp.route('/create', methods=['POST'])
def create():
    # Pun name, password required
    if 'pun_text' not in request.json or 'user_id' not in request.json:
        return abort(400)
    # construct Pun
    p = Pun(
        pun_text=request.json['pun_text'],
        user_id=request.json['user_id']
    )
    db.session.add(p)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(p.serialize())


@bp.route('/<int:pun_id>/category/<int:cat_id>', methods=['POST', 'DELETE'])
def modify_pun_categories(pun_id,cat_id):
    p = Pun.query.get(pun_id)
    c = Category.query.get(cat_id)

    
    if not p:
        return jsonify({'error': 'Pun not found'}), 404
    
    if not c:
        return jsonify({'error': 'Category not found'}), 404

    if request.method == 'POST':
        new_pun_cat = [{"pun_id": pun_id, "category_id": cat_id}]
        insert_pun_cat_query = puns_categories_table.insert().values(new_pun_cat)
        db.session.execute(insert_pun_cat_query)
        db.session.commit()
        return jsonify(p.serialize())
    elif request.method == 'DELETE':
        delete_pun_cat_query = puns_categories_table.delete().where(puns_categories_table.c.pun_id == pun_id).where(puns_categories_table.c.category_id == cat_id)
        result = db.session.execute(delete_pun_cat_query)
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'error':'Pun Category pairing does not exist.'}), 404
        return jsonify({'message': "Category removed."})




