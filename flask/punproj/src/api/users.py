from flask import Blueprint, jsonify, abort, request
from ..models import User, db
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
    # construct user
    u = User(
        user_name=request.json['user_name'],
        password=scramble(request.json['password'])
    )
    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(u.serialize())



