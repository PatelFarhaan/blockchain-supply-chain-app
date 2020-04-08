from project.models import Users
from flask_login import login_user
from flask import Blueprint, request, jsonify
from project.admin.admin_serializer import AdminSchema
from common_utilities.admin_json_schema import admin_login, admin_register
from werkzeug.security import generate_password_hash, check_password_hash

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        input_req = request.get_json()
        resp_obj = admin_login(input_req)
        if resp_obj["result"]:
            email = resp_obj["data"]["email"]
            password = resp_obj["data"]["password"]
            user = Users.objects.filter(email=email).first()

            if not user:
                return jsonify({"result": False, "message": "user does not exists"})

            if check_password_hash(user.password, password):
                login_user(user)
                ma_schema = AdminSchema()
                ret_obj = {"return": True}
                ret_obj["user_obj"] = ma_schema.dump(user)
                return ret_obj
            else:
                return jsonify({"result": False, "message": "incorrect password"})

        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        return jsonify({"result": True, "status_code": 200})


@admin_blueprint.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        input_req = request.get_json()
        resp_obj = admin_register(input_req)
        if resp_obj["result"]:
            email = input_req["email"]

            if Users.objects.filter(email=email).first():
                return jsonify({"result": False, "message": "user exists"})

            input_req["password"] = generate_password_hash(input_req["password"])
            input_req["is_admin"] = True
            new_user = Users(**input_req)
            new_user.save()

            return jsonify({"result": True, "message": "user created"})

        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        return jsonify({"result": True, "status_code": 200})
