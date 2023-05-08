from flask import Blueprint
from flask import jsonify 
from flask import abort
from flask import request
from ..models import Category, Pun, db
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
    cname = request.json['category_name']
    #check for dupes
    current_categories = Category.query.all()
    for cat in current_categories:
        if cat.category_name == cname:
            return abort(400, "Category already present.")
    # construct Category
    c = Category(
        category_name = cname
    )
    db.session.add(c)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(c.serialize())

@bp.route('/<int:id>/puns', methods=['GET'])
def category_pun_index(id: int):
    #return json of all puns in category
    category = Category.query.get(id)
    if not category:
        return abort(400, "Category not found.")
    cat_puns = category.get_all_puns()
    return jsonify(cat_puns)