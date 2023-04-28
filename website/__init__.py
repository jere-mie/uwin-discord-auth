import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dance.consumer import OAuth2ConsumerBlueprint

# getting config details
with open('config.json') as f:
    config = json.load(f)

# initializing Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config['secret_key']

# setting up SQLAlchemy connection (sqlite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = config['database_uri']
db = SQLAlchemy()
db.init_app(app)

# initializing authentication system
login_manager = LoginManager(app)
login_manager.login_view='home'

microsoft_blueprint = OAuth2ConsumerBlueprint(
    "microsoft",
    __name__,
    scope=["openid", "email", "profile", "User.Read"],
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    authorization_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    redirect_url=config['redirect_url']
)

app.register_blueprint(microsoft_blueprint, url_prefix="/login")

from website import routes
