import uuid
import datetime
from flask_login import UserMixin
from project import db, login_manager


@login_manager.user_loader
def user_load(user_id):
    return Users.objects.get(pk=user_id)


class Users(db.Document, UserMixin):
    user_id = db.StringField()
    password = db.StringField()
    is_admin = db.BooleanField(default=False)
    last_name = db.StringField(max_length=70)
    first_name = db.StringField(max_length=70)
    email = db.EmailField(required=True, unique=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow())

    meta = dict(indexes=['email', '-created'])


class Warehouse(db.Document):
    nodes = db.DictField()
    email = db.EmailField(required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow())

    meta = dict(indexes=['email'])


class Cargo(db.Document):
    cargos = db.DictField()
    email = db.EmailField(required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow())

    meta = dict(indexes=['email'])


class Sensor(db.Document):
    sensors = db.DictField()
    email = db.EmailField(required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow())

    meta = dict(indexes=['email'])