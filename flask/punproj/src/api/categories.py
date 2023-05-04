from flask import Blueprint
from flask import jsonify 
from flask import abort
from flask import request
from ..models import Category, db
from flask import current_app as app



bp = Blueprint('categories', __name__, url_prefix='/categories')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    categories = Category.query.all()  # ORM performs SELECT query
    result = []
    for c in categories:
        result.append(c.serialize())  # build list of questions as dictionaries
    return jsonify(result)  # return JSON response

@bp.route('/<int:id>', methods=['GET', 'DELETE'])
def show_or_delete(id: int):
    if request.method == 'GET':
        c = Category.query.get(id)
        return jsonify(c.serialize())
    elif request.method == 'DELETE':
        c = Category.query.get_or_404(id)
        try:
            db.session.delete(c)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)


@bp.route('/create', methods=['POST'])
def create():
    # Category name, password required
    if 'category_name' not in request.json:
        return abort(400)
    # construct Category
    c = Category(
        category_name=request.json['category_name']
    )
    db.session.add(c)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(c.serialize())