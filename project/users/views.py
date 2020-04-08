from common_utilities.cargo_json_schema import validate_user_cargo
from project.models import Users, Warehouse, Cargo
from flask_login import login_user, current_user, login_required, logout_user
from flask import Blueprint, request, jsonify
from project.users.users_serializer import UserSchema
from common_utilities.user_json_schema import user_login, user_register
from common_utilities.warehouse_json_schema import validate_user_warehouse
from werkzeug.security import generate_password_hash, check_password_hash

users_blueprint = Blueprint('user', __name__, url_prefix='/user')


@users_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        input_req = request.get_json()
        resp_obj = user_login(input_req)
        if resp_obj["result"]:
            email = resp_obj["data"]["email"]
            password = resp_obj["data"]["password"]
            user = Users.objects.filter(email=email).first()

            if not user:
                return jsonify({"result": False, "message": "user does not exists"})

            if check_password_hash(user.password, password):
                login_user(user)
                ma_schema = UserSchema()
                ret_obj = {"return": True}
                ret_obj["user_obj"] = ma_schema.dump(user)
                return ret_obj
            else:
                return jsonify({"result": False, "message": "incorrect password"})

        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        return jsonify({"result": True, "status_code": 200})


@users_blueprint.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        input_req = request.get_json()
        resp_obj = user_register(input_req)
        print(resp_obj, "\n\n\n\n\n\n")
        if resp_obj["result"]:
            print(input_req)
            email = input_req["email"]

            if Users.objects.filter(email=email).first():
                return jsonify({"result": False, "message": "user exists"})

            input_req["password"] = generate_password_hash(input_req["password"])
            new_user = Users(**input_req)
            new_user.save()

            return jsonify({"result": True, "message": "user created"})

        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        return jsonify({"result": True, "status_code": 200})


@users_blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    user_obj = current_user()
    logout_user(user_obj)


@users_blueprint.route('/warehouse', methods=["GET", "POST"])
@login_required
def warehouse():
    if request.method == "POST":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        input_req = request.get_json()
        resp_obj = validate_user_warehouse(input_req)

        if resp_obj["result"]:

            email = user_obj.email
            warehouse_obj = Warehouse.objects.filter(email=email).first()

            if not warehouse_obj:
                nodes = {input_req["name"]: input_req["location"]}
                new_warehouse_obj = Warehouse(nodes=nodes, email=email)
                new_warehouse_obj.save()
                return jsonify({"result": True, "message": "warehouse object created"})
            else:
                warehouse_obj.nodes[input_req["name"]] = input_req["location"]
                warehouse_obj.save()
                return jsonify({"result": True, "message": "warehouse object created"})

        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        warehouse_obj = Warehouse.objects.filter(email=user_obj.email).first()
        if not warehouse_obj:
            return jsonify({"result": False, "message": "warehouses do not exist"})

        res = []
        for k, v in warehouse_obj.nodes.items():
            res.append({"name": k, "location": v})

        return jsonify({"result": True, "data": res})


@users_blueprint.route('/cargo', methods=["GET", "POST"])
@login_required
def cargo():
    if request.method == "POST":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        input_req = request.get_json()
        resp_obj = validate_user_cargo(input_req)

        if resp_obj["result"]:
            email = user_obj.email
            cargo_obj = Cargo.objects.filter(email=email).first()

            if not cargo_obj:
                names_set = {input_req["name"]}
                new_cargo_obj = Cargo(names=names_set, email=email)
                new_cargo_obj.save()
                return jsonify({"result": True, "message": "cargo object created"})
            else:
                cargo_obj.names.add(input_req["name"])
                cargo_obj.save()
                return jsonify({"result": True, "message": "cargo object created"})

        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        cargo_obj = Cargo.objects.filter(email=user_obj.email).first()
        if not cargo_obj:
            return jsonify({"result": False, "message": "cargos do not exist"})

        res = []
        for name in cargo_obj.nodes.items():
            res.append({"name": name})

        return jsonify({"result": True, "data": res})
