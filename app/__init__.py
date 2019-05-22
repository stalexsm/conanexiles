from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Bundle, Environment
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from config import config

assets = Environment()
moment = Moment()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    assets.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    js = Bundle('js/jquery.js', 'js/bootstrap.js', filters='jsmin', output='assets/packed.js')
    css = Bundle('css/bootstrap.css', 'css/bootstrap-theme.css', 'css/styles.css', filters='cssmin', output='assets/packed.css')
    assets.register('js_all', js)
    assets.register('css_all', css)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
