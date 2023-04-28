import json
import urllib.parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dance.consumer import OAuth2ConsumerBlueprint

# getting config details
with open('config.json') as f:
    config = json.load(f)

# initializing Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config['flask_secret_key']

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
    client_id=config['azure_client_id'],
    client_secret=config['azure_client_secret'],
    authorization_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    redirect_url=config['azure_redirect_url']
)

app.register_blueprint(microsoft_blueprint, url_prefix="/login")

DISCORD_AUTH_URL = f'https://discord.com/api/oauth2/authorize?client_id={config["discord_client_id"]}&redirect_uri={urllib.parse.quote(config["discord_redirect_url"])}&response_type=code&scope=identify%20guilds.join'
from website import routes
