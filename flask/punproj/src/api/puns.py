from flask import Blueprint
from flask import jsonify
from flask import Blueprint
from flask import abort, request
from ..models import Pun
from flask import current_app as app

bp = Blueprint('puns', __name__, url_prefix='/puns')

@bp.route('', methods=['GET'])
def index():
    puns = Pun.query.all()
    results = []
    for p in puns:
        results.append(p.serialize())

    return jsonify(results)