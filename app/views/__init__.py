from . import topic
from . import misc
from . import cluster

from app import bp_main

@bp_main.after_request
def after_request(response):
    if response.headers['Content-Type'] == u'text/html; charset=utf-8':
        response.headers['Content-Type'] = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, x-token, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
    return response
