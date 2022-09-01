
from flask import Flask, Blueprint
import os

bp_main = Blueprint('main', __name__)
from . import views

def create_app():
    app = Flask(__name__)
    # 注册配置文件
    app.config.from_object('config.default')
    config_name = os.environ.get('ENV', None)
    if config_name:
        config_name = config_name.lower()
        app.config.from_object('config.{0}'.format(config_name))
    # 注册蓝图
    app.register_blueprint(bp_main, url_prefix=app.config.get('SERVER_URL_PREFIX', ''))
    return app
