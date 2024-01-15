from flask import Flask
from .extensions import db, migrate, bcrypt, login_manager
from .configurations import config

app = Flask(__name__)

def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from .home import home_blueprint
        from .auth import auth_blueprint
        from .account import account_blueprint
        from .todo import todo_blueprint
        from .cookies import cookies_blueprint

        app.register_blueprint(home_blueprint, url_prefix='/')
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(account_blueprint, url_prefix='/account')
        app.register_blueprint(todo_blueprint, url_prefix='/todo')
        app.register_blueprint(cookies_blueprint, url_prefix='/cookies')

        return app