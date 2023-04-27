import json
import sys
from flask import Flask, redirect, url_for, render_template
from flask_dance.consumer import OAuth2ConsumerBlueprint

with open('config.json', encoding="utf8") as f:
    config = json.load(f)

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

app = Flask(__name__)
app.secret_key = config['secret_key']
app.register_blueprint(microsoft_blueprint, url_prefix="/login")

@app.route("/authorized")
def microsoft_authorized():
    resp = microsoft_blueprint.session.get("https://graph.microsoft.com/v1.0/me")
    print(resp.json())
    if resp.ok:
        user_info = resp.json()
        email = user_info["mail"]
        name = user_info["displayName"]
        print(f"Authenticated as {name} ({email})")
        return "You are authenticated!"
    else:
        return "Authentication failed"

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    if len(sys.argv) < 1:
        app.run()
    else:
        # for development, we need SSL certs for localhost
        app.run(debug=True, ssl_context=("cert.pem", "key.pem"))
