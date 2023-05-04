from flask import Blueprint
from flask import jsonify
from flask import abort, request
from ..models import Pun, db
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



