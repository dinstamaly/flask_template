"""
TODO: документация
"""
import logging
import traceback

from flask import Flask, request, Response

import service
from core_lib.codes import MESSAGES, SYSTEM_ERROR
from core_lib.utils import (
    make_json_response, BusinessException, make_xml_response,
)
from core_lib.models import db


__author__ = 'Din'


app = Flask(__name__)
app.config.from_object('configuration')

db.init_app(app)


@app.errorhandler(BusinessException)
@app.errorhandler(Exception)
def core_error(e):
    code = ''

    if hasattr(e, 'code') and e.code:
        code = str(e.code)

    logging.error(traceback.format_exc() + code)

    if request.headers['Content-Type'] == 'application/json':

        if isinstance(e, BusinessException):

            if not e.message:
                e.message = MESSAGES.get('ru', {}).get(e.code, 'Server Error')

            return make_json_response({'result': e.code, 'message': e.message})

        if isinstance(e, KeyError):
            return make_json_response({
                'result': -20,
                'message': f'Обязательный параметр отсутствует: {e}',
            })

        return make_json_response({'result': SYSTEM_ERROR})

    if isinstance(e, BusinessException):
        return make_xml_response(p_code=e.code, p_message=e.message)

    if isinstance(e, KeyError):
        return make_xml_response(
            p_code=-20, p_message=f'Обязательный параметр отсутствует: {e}',
        )

    return make_xml_response(p_code=SYSTEM_ERROR)


@app.route('/discounts/<string:path>/<string:command>', methods=['POST'])
@app.route('/discounts/<string:path>.<string:command>', methods=['POST'])
def controller_ws(path, command):
    data = request.json or {}
    ret = service.call(f'{path}.{command}', data)

    if isinstance(ret, Response):
        return ret

    return make_json_response(ret)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
