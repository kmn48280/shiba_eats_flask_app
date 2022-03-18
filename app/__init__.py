from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_cors import CORS
import os


### LOGIN ###
login = LoginManager()

### DB SQL ###

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()



def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    ### DEPLOYMENT ###
    if os.environ.get('FLASK_ENV') == 'development':
        cors = CORS
    
    ### LOGIN ERRORS/VIEW ###
    login.login_view = 'auth.login'
    login.login_message = 'Woof! Woof!! Please Login before viewing contents of this page'
    login.login_message_category = 'warning'

    
    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    from .bueprints.social import bp as social_bp
    app.register_blueprint(social_bp)

    return app
    
    

    







