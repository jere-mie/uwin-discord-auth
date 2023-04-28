from website import app, db
import os
import json
import sys

# getting config details
with open('config.json') as f:
    config = json.load(f)

# initializing db if it doesn't exist yet (change this if not using sqlite)
if not os.path.exists("instance/site.db"):
    with app.app_context():
        db.create_all()

# running debug site
if __name__=='__main__':
    # run this command with any additional arg to run in production
    if len(sys.argv) > 1:
        print('<< PROD >>')
        os.system(f"gunicorn -b '0.0.0.0:{config['port']}' website:app")
    # or just run without an additional arg to run in debug
    else:
        print('<< DEBUG >>')
        app.run(debug=True, ssl_context=("cert.pem", "key.pem"))
