import json
from functools import wraps
from os import path

from flask import request, make_response, jsonify
from schema import SchemaError

def validate_params(schema):
    """
    Decorator that retrieves the arguments from the request
    validates them with the corresponding schema and the returns
    the whole method with the parameters.
    """
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                params = request.args.to_dict(flat=True)
                if request.method != 'GET':
                    try:
                        params.update(json.loads(request.get_data()).copy())
                    except:
                        params.update(request.form.to_dict(flat=True))
                        params.update(request.files.to_dict(flat=True))
                schema.validate(params)
            except SchemaError as error:
                return make_response(
                    jsonify({'error': error.code}), 400)
            return func(params)
        return wrapped

    return decorator