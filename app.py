from flask import blueprints, Blueprint, Flask
from flask_session import Session
from app.routes import routes
from app.admin_routes import admin
from app import db, admin_db

db.init_db()
# print(app.admin_db.__file__)
admin_db.init_admin()

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'blaalaldjsdjfinsdkjffdnfkjefjnffijsiojojdf'

Session(app)

app.register_blueprint(routes)
app.register_blueprint(admin)

app.run(debug=True, host='0.0.0.0')