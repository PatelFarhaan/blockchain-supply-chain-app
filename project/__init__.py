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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = MongoEngine(app)
ma = Marshmallow(app)
CORS(app)

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
