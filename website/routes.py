from flask import render_template
from flask_login import login_user
from website import app, microsoft_blueprint, db
from website.models import User

@app.route("/authorized")
def microsoft_authorized():
    resp = microsoft_blueprint.session.get("https://graph.microsoft.com/v1.0/me")
    if resp.ok:
        # retrieved user info
        user_info = resp.json()
        email = user_info["mail"]
        name = user_info["displayName"]

        # if user exists we simply log them in, else we create a new user and log them in
        user = User.query.filter_by(email=email).first()
        if user is None:
            print("Creating new user")
            user = User(email=email, name=name)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        print(f"Authenticated as {user}")
        return "You are authenticated!"
    else:
        return "Authentication failed"

@app.route("/")
def home():
    return render_template('home.html')
