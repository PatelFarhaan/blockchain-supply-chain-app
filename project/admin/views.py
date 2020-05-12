from project.models import Users, Warehouse
from flask import Blueprint, request, jsonify
from project.admin.admin_serializer import AdminSchema, UserObj
from werkzeug.security import generate_password_hash, check_password_hash
from common_utilities.admin_json_schema import admin_login, admin_register
from flask_login import login_user, login_required, logout_user, current_user

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


@admin_blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"result": True, "message": "admin logged out"})


@admin_blueprint.route('/warehouse', methods=["GET", "POST"])
@login_required
def warehouse():
    if request.method == "POST":
        return jsonify(True)

    elif request.method == "GET":

        warehouse_obj = Warehouse.objects.all()

        if not warehouse_obj:
            return jsonify({"result": False, "message": "warehouses do not exist"})

        res = []
        for i in warehouse_obj:
            for k, v in i.nodes.items():
                res.append({"email": i.email, "name": k, "location": v})

        return jsonify({"result": True, "data": res})


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


@admin_blueprint.route('/users', methods=["GET"])
@login_required
def all_users():
    if request.method == "GET":
        all_users = Users.objects.all()
        ma_schema = UserObj()
        resp = ma_schema.dump(all_users, many=True)
        return jsonify({"result": True, "data": resp})


@admin_blueprint.route('/delete-user', methods=["DELETE"])
@login_required
def delete_users():
    if request.method == "DELETE":
        inp_req = request.get_json()
        email = inp_req["email"]

        user_obj = Users.objects.filter(email=email).first()
        if user_obj is None:
            return jsonify({"result": False, "message": "user does not exist"})

        user_obj.delete()
        user_obj.save()
        return jsonify({"result": True, "message": "user deleted"})