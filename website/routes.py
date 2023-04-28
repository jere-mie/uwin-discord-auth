import json
import requests
from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from website import app, microsoft_blueprint, db, DISCORD_AUTH_URL, config
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
            user = User(email=email, name=name)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('discord_auth'))
    else:
        return "Authentication failed"

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('discord_auth'))
    return render_template('home.html')

@app.route("/discordauth")
@login_required
def discord_auth():
    return render_template('discord.html', url=DISCORD_AUTH_URL)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/discord/authorized')
def discord_authorized():
    # Exchange the authorization code for an access token
    response = requests.post('https://discordapp.com/api/oauth2/token', 
                             headers={'Content-type': 'application/x-www-form-urlencoded'}, 
                             data={
        'client_id': config['discord_client_id'],
        'client_secret': config['discord_client_secret'],
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
        'redirect_uri': config['discord_redirect_url'],
        'scope': 'identify%20guilds.join'
    })
    token_data = json.loads(response.text)
    access_token = token_data['access_token']
    user_id = get_discord_user_id(access_token)
    if current_user.discord_id is not None and user_id != current_user.discord_id:
        return '<h1>Error - This UWindsor Account is already associated with a different Discord account</h1><p>Contact a site administrator for more information</p>'
    add_user_to_server(user_id, config['discord_server_id'], access_token, current_user.name)
    current_user.discord_id = user_id
    db.session.commit()
    return '<h1>Success!</h1><p>Your account has been added to the server. You can now close this window</p>'

def add_user_to_server(user_id, server_id, access_token, nickname):
    # Add the specified user to the specified server
    headers = {
        'Authorization': 'Bot ' + config['discord_bot_token'],
        'Content-Type': 'application/json'
    }
    data = {
        'access_token': access_token,
        'nick': nickname
    }
    response = requests.put('https://discordapp.com/api/guilds/' + server_id + '/members/' + user_id, headers=headers, data=json.dumps(data))
    return response.status_code == 201

def get_discord_user_id(access_token):
    # Get the user's information from the Discord API
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get('https://discordapp.com/api/users/@me', headers=headers)
    user_info = json.loads(response.text)
    return user_info['id']