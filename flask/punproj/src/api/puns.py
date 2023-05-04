from flask import Blueprint
from flask import jsonify
from flask import Blueprint

from flask.punproj.src.models import Pun

bp = Blueprint('pun', __name__, url_prefix='/pun')

# Get all puns
@bp.route('/puns', methods=['GET'])
def get_all_puns():
    puns = Pun.query.all()
    results = [
        {
            "pun_id": pun.id,
            "pun_text": pun.pun_text,
            "author_id": pun.user_id
        } for pun in puns]

    return 'jsonify(results)'