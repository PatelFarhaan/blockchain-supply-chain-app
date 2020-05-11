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
    size = db.StringField()
    address = db.StringField()
    active = db.BooleanField()
    latitude = db.StringField()
    longitude = db.StringField()
    cargo_capacity = db.IntegerField()
    email = db.EmailField(required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow())

    meta = dict(indexes=['email'])


class Cargo(db.Document):
    names = db.DictField()
    source = db.StringField()
    sensor_id = db.StringField()
    driver_age = db.StringField()
    driver_name = db.StringField()
    destination = db.StringField()
    email = db.EmailField(required=True)
    cargo_registration = db.StringField()
    source_warehouse_id = db.StringField()
    driver_license_number = db.StringField()
    destination_warehouse_id = db.StringField()
    created = db.DateTimeField(default=datetime.datetime.utcnow())

    meta = dict(indexes=['email'])

class Sensor(db.Document):
    cargo = db.StringField()
    weight = db.StringField()
    locations = db.ListField()
    active = db.BooleanField()
    latitude = db.StringField()
    warehouse = db.StringField()
    longitude = db.StringField()
    barcode_id = db.StringField()
    temperature = db.StringField()
    sensor_type = db.StringField()
    email = db.EmailField(required=True)
    sensorid = db.StringField(default=str(uuid.uuid4()))

    meta = dict(indexes=['sensorid'])