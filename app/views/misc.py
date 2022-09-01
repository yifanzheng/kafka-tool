
from flask import current_app

from app import bp_main


@bp_main.get('/version')
def version():
    return current_app.config['VERSION']


@bp_main.get('/faq')
def faq():
    return '<!--KafkaCenter-->'
