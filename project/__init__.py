import sys
sys.path.append("../")
from flask import Flask
from flask_login import LoginManager
from common_utilities import CONSTANT
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow


######################################   *** :=>  CONFIG  <=: ***   #########################################

app = Flask(__name__)
app.config['SECRET_KEY'] = CONSTANT.SECRET_KEY.value

app.config['MONGODB_SETTINGS'] = {'host': CONSTANT.PRIMARY_DB_CLUSTER.value}
db = MongoEngine(app)
ma = Marshmallow(app)

login_manager = LoginManager(app)
login_manager.login_view = "user.login"

######################################   *** :=>  BLUEPRINT  <=: ***   #########################################