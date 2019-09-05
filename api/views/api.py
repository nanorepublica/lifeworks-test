import typing
from datetime import datetime

from flask import Blueprint, jsonify, make_response, request

from ..models import Event

bp = Blueprint('api', __name__, url_prefix='/api')


def api_get() -> typing.Tuple:
    name = 'some_event'
    to_param, from_param, location_param = None, None, None
    if not request.args:
        return (
            {
                "status": "error",
                'message': "request must have at least one of: 'from', 'to' or 'location'"
            },
            400
        )
    if 'to' in request.args.keys():
        to_param = datetime.fromtimestamp(int(request.args['to']))
    if 'from' in request.args.keys():
        from_param = datetime.fromtimestamp(int(request.args['from']))
    if 'location' in request.args.keys():
        location_param = request.args['location']

    result_set = Event.query(name, from_param, to_param, location_param)
    results = list(result_set)
    return jsonify(results), 200


def api_post() -> typing.Tuple:
    # TODO: validation on incoming data
    # TODO: contact geo ip API (as a task?)
    data = request.json
    event = Event(**data)
    success = event.save()
    if not success:
        return {"status": "error", 'message': 'error writing to database'}, 500
    return {"status": "success", "data": next(event.get_self_from_db())}, 201


@bp.route('/event', methods=['POST', 'GET'])
def api():
    http_method_function = {
        'get': api_get,
        'post': api_post
    }
    method_func = http_method_function.get(request.method.lower())
    if not method_func:
        # error 405
        return make_response(({"status": "error", 'message': 'bad method'}, 405))
    resp, status = method_func()
    if resp:
        return make_response(resp, status)
    return make_response(({"status": "error", 'message': 'bad request'}, 400))
