from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Pun, ratings_table
from flask import current_app as app
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('users', __name__, url_prefix='/users')



@bp.route('/all', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    users = User.query.all()  # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize())  # build list of questions as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET', 'DELETE'])
def show_or_delete(id: int):
    if request.method == 'GET':
        u = User.query.get(id)
        return jsonify(u.serialize())
    elif request.method == 'DELETE':
        u = User.query.get_or_404(id)
        try:
            db.session.delete(u)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)


@bp.route('/create', methods=['POST'])
def create():
    # user name, password required
    if 'user_name' not in request.json or 'password' not in request.json:
        return abort(400)
    # check for dupes
    new_uname = request.json['user_name']
    current_users = User.query.all()
    for current_u in current_users:
        if current_u.user_name == new_uname:
            return abort(400, "Username already taken.")
    u = User(
        user_name=new_uname,
        password=scramble(request.json['password'])
    )
    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(u.serialize())


@bp.route('/<int:id>/puns', methods=['GET'])
def user_pun_index(id: int):
    #return json of all puns credited to id user
    user = User.query.get(id)
    if not user:
        return abort(400, "User not found.")
    user_puns = user.get_all_puns()
    return jsonify(user_puns)



