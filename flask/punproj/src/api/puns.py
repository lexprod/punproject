from flask import Blueprint
from flask import jsonify
from flask import abort, request
from ..models import Pun, User, db, ratings_table
from flask import current_app as app

bp = Blueprint('puns', __name__, url_prefix='/puns')

@bp.route('', methods=['GET'])
def index():
    puns = Pun.query.all()
    results = []
    for p in puns:
        results.append(p.serialize())

    return jsonify(results)


@bp.route('/<int:id>', methods=['GET', 'DELETE'])
def show_or_delete(id: int):
    if request.method == 'GET':
        p = Pun.query.get(id)
        return jsonify(p.serialize())
    elif request.method == 'DELETE':
        p = Pun.query.get_or_404(id)
        try:
            db.session.delete(p)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)
        

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


