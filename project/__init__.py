import sys
sys.path.append("../")
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from common_utilities import CONSTANT
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from common_utilities.wallet import Wallet
from common_utilities.blockchain import Blockchain

######################################   *** :=>  CONFIG  <=: ***   #########################################
app = Flask(__name__)
app.config['SECRET_KEY'] = CONSTANT.SECRET_KEY.value
app.config['MONGODB_SETTINGS'] = {'host': CONSTANT.PRIMARY_DB_CLUSTER.value}

CORS(app, support_credentials=True, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
db = MongoEngine(app)
ma = Marshmallow(app)
CORS(app)


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

login_manager = LoginManager(app)
login_manager.login_view = "user.login"

wallet = Wallet(CONSTANT.PORT.value)
blockchain = Blockchain(wallet.public_key, CONSTANT.PORT.value)

######################################   *** :=>  BLUEPRINT  <=: ***   ########################################
from project.users.views import users_blueprint
from project.admin.views import admin_blueprint
from project.blockchain.views import blockchain_blueprint
from project.error.error_handler import errorpage_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(errorpage_blueprint)
app.register_blueprint(blockchain_blueprint)