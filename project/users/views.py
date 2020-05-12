import json
import uuid
import requests
import polyline
from random import randint
from datetime import datetime
from common_utilities import CONSTANT
from flask import Blueprint, request, jsonify
from project.users.users_serializer import UserSchema, UserObj
from common_utilities.cargo_json_schema import validate_user_cargo
from common_utilities.sensor_json_schema import validate_user_sensor
from project.models import Users, Warehouse, Cargo, Sensor, BlockChain
from common_utilities.user_json_schema import user_login, user_register
from werkzeug.security import generate_password_hash, check_password_hash
from common_utilities.warehouse_json_schema import validate_user_warehouse
from flask_login import login_user, current_user, login_required, logout_user


port = CONSTANT.PORT.value
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


@users_blueprint.route('/mobile/login', methods=["GET", "POST"])
def mobile_login():
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
                ret_obj = {"result": True}
                ret_obj["data"] = ma_schema.dump(user)
                ret_obj["data"]["id"] = user.user_id
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
        if resp_obj["result"]:
            print(input_req)
            email = input_req["email"]

            if Users.objects.filter(email=email).first():
                return jsonify({"result": False, "message": "user exists"})

            input_req["password"] = generate_password_hash(input_req["password"])
            input_req["user_id"] = str(uuid.uuid4())
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
    logout_user()
    return jsonify({"result": True, "message": "user logged out"})


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
                temp_obj = {
                    "name": input_req["name"],
                    "address": input_req["address"],
                    "size": input_req["size"],
                    "active": input_req["active"],
                    "latitude": input_req["latitude"],
                    "longitude": input_req["longitude"],
                    "location": input_req["location"],
                    "cargo_capacity": input_req["cargo_capacity"]
                }
                nodes = {input_req["name"]: temp_obj}
                new_warehouse_obj = Warehouse(nodes=nodes, email=email)
                new_warehouse_obj.save()
                return jsonify({"result": True, "message": "warehouse object created"})
            else:
                temp_obj = {
                    "name": input_req["name"],
                    "address": input_req["address"],
                    "size": input_req["size"],
                    "active": input_req["active"],
                    "latitude": input_req["latitude"],
                    "longitude": input_req["longitude"],
                    "location": input_req["location"],
                    "cargo_capacity": input_req["cargo_capacity"]
                }
                warehouse_obj.nodes[input_req["name"]] = temp_obj
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
            temp_obj = {}
            temp_obj["name"] = k
            for i,j in v.items():
                temp_obj[i] = j
            res.append(temp_obj)

        return jsonify({"result": True, "data": res})


@users_blueprint.route('mobile/warehouse/<user_id>', methods=["GET", "POST"])
def mobile_warehouse(user_id):
    if request.method == "POST":
        user_obj = Users.objects.filter(user_id=user_id).first()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        input_req = request.get_json()
        resp_obj = validate_user_warehouse(input_req)

        if resp_obj["result"]:

            email = user_obj.email
            warehouse_obj = Warehouse.objects.filter(email=email).first()

            if not warehouse_obj:
                temp_obj = {
                    "name": input_req["name"],
                    "address": input_req["address"],
                    "size": input_req["size"],
                    "active": input_req["active"],
                    "latitude": input_req["latitude"],
                    "longitude": input_req["longitude"],
                    "location": input_req["location"],
                    "cargo_capacity": input_req["cargo_capacity"]
                }
                nodes = {input_req["name"]: temp_obj}
                new_warehouse_obj = Warehouse(nodes=nodes, email=email)
                new_warehouse_obj.save()
                return jsonify({"result": True, "message": "warehouse object created"})
            else:
                temp_obj = {
                    "name": input_req["name"],
                    "address": input_req["address"],
                    "size": input_req["size"],
                    "active": input_req["active"],
                    "latitude": input_req["latitude"],
                    "longitude": input_req["longitude"],
                    "location": input_req["location"],
                    "cargo_capacity": input_req["cargo_capacity"]
                }
                warehouse_obj.nodes[input_req["name"]] = temp_obj
                warehouse_obj.save()
                return jsonify({"result": True, "message": "warehouse object created"})

        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        user_obj = Users.objects.filter(user_id=user_id).first()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        warehouse_obj = Warehouse.objects.filter(email=user_obj.email).first()
        if not warehouse_obj:
            return jsonify({"result": False, "message": "warehouses do not exist"})

        res = []
        for k, v in warehouse_obj.nodes.items():
            temp_obj = {}
            temp_obj["name"] = k
            for i, j in v.items():
                temp_obj[i] = j
            res.append(temp_obj)

        return jsonify({"result": True, "data": res})


@users_blueprint.route('/warehouse/<w_name>', methods=["DELETE"])
@login_required
def delete_warehouse(w_name):
    if request.method == "DELETE":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        warehouse_obj = Warehouse.objects(email=user_obj.email).first()

        if not warehouse_obj:
            return jsonify({"result": False, "message": "warehouse does not exists"})
        else:
            warehouse_nodes = dict(warehouse_obj.nodes)

            if not w_name in warehouse_nodes:
                return jsonify({"result": False, "message": "warehouse does not exist"})

            del warehouse_nodes[w_name]
            warehouse_obj.nodes = warehouse_nodes
            warehouse_obj.save()
            return jsonify({"result": True, "message": "warehouse deleted"})


@users_blueprint.route('/mobile/warehouse/<user_id>/<w_name>', methods=["DELETE"])
def mobile_delete_warehouse(user_id, w_name):
    if request.method == "DELETE":
        user_obj = Users.objects.filter(user_id=user_id).first()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        warehouse_obj = Warehouse.objects(email=user_obj.email).first()

        if not warehouse_obj:
            return jsonify({"result": False, "message": "warehouse does not exists"})
        else:
            warehouse_nodes = dict(warehouse_obj.nodes)

            if not w_name in warehouse_nodes:
                return jsonify({"result": False, "message": "warehouse does not exist"})

            del warehouse_nodes[w_name]
            warehouse_obj.nodes = warehouse_nodes
            warehouse_obj.save()
            return jsonify({"result": True, "message": "warehouse deleted"})


@users_blueprint.route('/sensor', methods=["GET", "POST", "PATCH"])
@login_required
def sensor():
    if request.method == "POST":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        input_req = request.get_json()
        resp_obj = validate_user_sensor(input_req)

        if resp_obj["result"]:
            email = user_obj.email

            sensor_obj = Sensor.objects.filter(email=email).first()
            if sensor_obj is None:
                sensor_id = str(uuid.uuid4())
                sensor_data = {}
                del input_req["sensor_id"]
                sensor_data[sensor_id] = input_req
                sensor_obj = Sensor(email=email, sensors=sensor_data)
                sensor_obj.save()
                return jsonify({"result": True, "message": "sensor object created"})
            else:
                sensor_dict = dict(sensor_obj.sensors)
                sensor_id = str(uuid.uuid4())
                del input_req["sensor_id"]
                sensor_dict[sensor_id] = input_req
                sensor_obj.sensors = sensor_dict
                sensor_obj.save()
                return jsonify({"result": True, "message": "sensor object created"})
        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        sensor_obj = Sensor.objects.filter(email=user_obj.email).first()
        if not sensor_obj:
            return jsonify({"result": False, "message": "No sensors found for this user"})

        res = []
        data = sensor_obj.sensors
        for k,v in data.items():
            temp_obj = {}
            temp_obj["sensor_id"] = k
            for i,j in v.items():
                temp_obj[i] = j
            res.append(temp_obj)
        return jsonify({"result": True, "data": res})


@users_blueprint.route('mobile/sensor/<user_id>', methods=["GET", "POST", "PATCH"])
def mobile_sensor(user_id):
    if request.method == "POST":
        user_obj = Users.objects.filter(user_id=user_id).first()

        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        input_req = request.get_json()
        resp_obj = validate_user_sensor(input_req)

        if resp_obj["result"]:
            email = user_obj.email

            sensor_obj = Sensor.objects.filter(email=email).first()
            if sensor_obj is None:
                sensor_id = str(uuid.uuid4())
                sensor_data = {}
                del input_req["sensor_id"]
                sensor_data[sensor_id] = input_req
                sensor_obj = Sensor(email=email, sensors=sensor_data)
                sensor_obj.save()
                return jsonify({"result": True, "message": "sensor object created"})
            else:
                sensor_dict = dict(sensor_obj.sensors)
                sensor_id = str(uuid.uuid4())
                del input_req["sensor_id"]
                sensor_dict[sensor_id] = input_req
                sensor_obj.sensors = sensor_dict
                sensor_obj.save()
                return jsonify({"result": True, "message": "sensor object created"})
        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        user_obj = Users.objects.filter(user_id=user_id).first()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        sensor_obj = Sensor.objects.filter(email=user_obj.email).first()
        if not sensor_obj:
            return jsonify({"result": False, "message": "No sensors found for this user"})

        res = []
        data = sensor_obj.sensors
        for k, v in data.items():
            temp_obj = {}
            temp_obj["sensor_id"] = k
            for i, j in v.items():
                temp_obj[i] = j
            res.append(temp_obj)
        return jsonify({"result": True, "data": res})

@users_blueprint.route('cargo/<cargoid>', methods=["GET"])
@login_required
def getmapdetails(cargoid):
    if request.method == "GET":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        cargo_obj = Cargo.objects.filter(email=user_obj.email).first()
        if not cargo_obj:
            return jsonify({"result": False, "message": "cargo's do not exist"})

        route_id = str(uuid.uuid4())
        res = []
        data = cargo_obj.cargos
        cargo = {}
        for i in data.keys():
            if i == cargoid:
                cargo = data[i]
        source = cargo['source']
        destination = cargo['destination']
        if source == 'San Jose':
            source = '37.774929,-122.419418'
        elif source == 'Chicago':
            source = "41.8781,-87.6298"
        elif source == 'New York':
            source = "40.7128,-74.0060" 
        elif source == 'Boston':
            source = "42.3601,-71.0589"
        
        if destination == 'San Jose':
            destination = '37.774929,-122.419418'
        elif destination == 'Chicago':
            destination = "41.8781,-87.6298"
        elif destination == 'New York':
            destination = "40.7128,-74.0060" 
        elif destination == 'Boston':
            destination = "42.3601,-71.0589"

        try:
            api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + source + '&destination=' + destination + '&key=' + api_key
            response = requests.get(api_url)
            json_data = json.loads(response.text)
            if not json_data['routes'][0]:
                return jsonify({"result": True, "message": "No route exists between source and destination"})

            steps = json_data['routes'][0]['overview_polyline']['points']
            steps = polyline.decode(steps)
            return jsonify({"result": True, "data": {"locations": steps, "cargo":cargo,"route_id":route_id}})

        except:
            return jsonify({"result": True, "message": "Cannot connect to Google Maps"})



        return jsonify({"result": True, "data": cargo})



@users_blueprint.route('/cargo', methods=["GET", "POST", "DELETE"])
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
            car_obj = Cargo.objects.filter(email=email).first()
            if car_obj is None :
                input_req["email"] = email
                cargos_data = {}
                cargo_id = str(uuid.uuid4())
                cargos_data[cargo_id] = input_req
                new_cargo = Cargo(email=email, cargos=cargos_data)
                new_cargo.save()
                return jsonify({"result": True, "message": "cargo object created"})
            else:
                cargos_dict = dict(car_obj.cargos)
                cargo_id = str(uuid.uuid4())
                cargos_dict[cargo_id] = input_req
                car_obj.cargos = cargos_dict
                car_obj.save()
                return jsonify({"result": True, "message": "cargo object created"})
        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        cargo_obj = Cargo.objects.filter(email=user_obj.email).first()
        if not cargo_obj:
            return jsonify({"result": False, "message": "cargo's do not exist"})

        res = []
        data = cargo_obj.cargos
        for k, v in data.items():
            temp_obj = {}
            temp_obj["cargo_id"] = k
            for i, j in v.items():
                temp_obj[i] = j
            res.append(temp_obj)
        return jsonify({"result": True, "data": res})


@users_blueprint.route('/mobile/cargo/<user_id>', methods=["GET", "POST", "DELETE"])
def mobile_cargo(user_id):
    if request.method == "POST":
        user_obj = Users.objects.filter(user_id=user_id).first()

        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        input_req = request.get_json()
        resp_obj = validate_user_cargo(input_req)

        if resp_obj["result"]:
            email = user_obj.email
            car_obj = Cargo.objects.filter(email=email).first()
            if car_obj is None:
                input_req["email"] = email
                cargos_data = {}
                cargo_id = str(uuid.uuid4())
                cargos_data[cargo_id] = input_req
                new_cargo = Cargo(email=email, cargos=cargos_data)
                new_cargo.save()
                return jsonify({"result": False, "message": "cargo object created"})
            else:
                cargos_dict = dict(car_obj.cargos)
                cargo_id = str(uuid.uuid4())
                cargos_dict[cargo_id] = input_req
                car_obj.cargos = cargos_dict
                car_obj.save()
                return jsonify({"result": False, "message": "cargo object created"})
        else:
            return jsonify(resp_obj)

    elif request.method == "GET":
        user_obj = Users.objects.filter(user_id=user_id).first()

        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        cargo_obj = Cargo.objects.filter(email=user_obj.email).first()
        if not cargo_obj:
            return jsonify({"result": False, "message": "cargo's do not exist"})

        res = []
        data = cargo_obj.cargos
        for k, v in data.items():
            temp_obj = {}
            temp_obj["cargo_id"] = k
            for i, j in v.items():
                temp_obj[i] = j
            res.append(temp_obj)
        return jsonify({"result": True, "data": res})


@users_blueprint.route('/mobile/user-bill/<user_id>', methods=["GET"])
def bill_user(user_id):
    if request.method == "GET":
        all_users = Users.objects.filter(user_id=user_id).first()
        if all_users is None:
            return jsonify({"result": False, "message": "no users exist"})

        res = []
        ma_schema = UserObj()
        i = ma_schema.dump(all_users)
        try:
            break_down, total = helper(all_users.email)
            i["blockchain_nodes"] = break_down["blockchain_nodes"]
            i["cargo_blocks"] = break_down["cargo_blocks"]
            i["upfront_fee"] = break_down["upfront_fee"]
            i["total"] = total
            res.append(i)
        except:
            pass
        return jsonify({"result": True, "data": res})


def helper(email):
    cargo_obj = Cargo.objects.filter(email=email).first()
    bc_obj = BlockChain.objects.filter(email=email).first()
    block_len = len(bc_obj.blocks)
    cargos_len = len(cargo_obj.cargos)
    res = {
        "blockchain_nodes": block_len,
        "cargo_blocks": cargos_len,
        "upfront_fee": "$10"
    }
    total = 10 + (block_len+cargos_len) * 0.10
    return res, total
########################################################################################


@users_blueprint.route('/cargo/<cid>', methods=["DELETE"])
@login_required
def delete_cargo(cid):
    if request.method == "DELETE":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        cargo_obj = Cargo.objects(email=user_obj.email).first()

        if not cargo_obj:
            return jsonify({"result": False, "message": "cargo does not exists"})
        else:
            del cargo_obj.names[cid]
            cargo_obj.save()
            return jsonify({"result": True, "message": "cargo deleted"})


@users_blueprint.route('/mobile/cargo/<user_id>/<cid>', methods=["DELETE"])
@login_required
def mobile_delete_cargo(user_id, cid):
    if request.method == "DELETE":
        user_obj = Users.objects.filter(user_id=user_id).first()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        cargo_obj = Cargo.objects(email=user_obj.email).first()

        if not cargo_obj:
            return jsonify({"result": False, "message": "cargo does not exists"})
        else:
            del cargo_obj.names[cid]
            cargo_obj.save()
            return jsonify({"result": True, "message": "cargo deleted"})


@users_blueprint.route('/deletesensor/<id>', methods=["DELETE"])
@login_required
def deletesensor(id):
    if request.method == "DELETE":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        sensorid = id
        Sensor.objects(email=user_obj.email, sensorid=sensorid).delete()

        return jsonify({"result": True, "message": "sensor deleted"})


@users_blueprint.route('mobile/deletesensor/<user_id>/<id>', methods=["DELETE"])
@login_required
def mobile_deletesensor(user_id, id):
    if request.method == "DELETE":
        user_obj = Users.objects.filter(user_id=user_id).first()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        sensorid = id
        Sensor.objects(email=user_obj.email, sensorid=sensorid).delete()

        return jsonify({"result": True, "message": "sensor deleted"})




@users_blueprint.route('/cargo/<name>', methods=["POST"])
@login_required
def updatecargo(name):
    if not name:
        return jsonify({"result": False, "message": "Invalid cargo name"})

    if request.method == "POST":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})
        cargo = Cargo.objects.filter(email=user_obj.email).first()
        print('1234567890')
        input_req = request.get_json()
        source = input_req['source']
        destination = input_req['destination']
        # sensor = input_req['sensor']
        curr_cargo = cargo.names[name]

        curr_cargo['source'] = source
        curr_cargo['destination'] = destination
        cargo.names[name] = curr_cargo
        cargo.save()

        res = []
        for i in cargo.names:
            res.append({i: cargo.names[i]})

        try:
            api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + source + '&destination=' + destination + '&key=' + "api_key"
            response = requests.get(api_url)
            json_data = json.loads(response.text)
            if not json_data['routes'][0]:
                return jsonify({"result": True, "message": "No route exists between source and destination"})

            steps = json_data['routes'][0]['overview_polyline']['points']
            steps = polyline.decode(steps)
            return jsonify({"result": True, "data": {"locations": steps}})

        except:
            return jsonify({"result": True, "message": "Cannot connect to Google Maps"})



@users_blueprint.route('mobile/cargo/<user_id>/<name>', methods=["POST"])
@login_required
def mobile_updatecargo(user_id, name):
    if not name:
        return jsonify({"result": False, "message": "Invalid cargo name"})

    if request.method == "POST":
        user_obj = Users.objects.filter(user_id=user_id).first()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        cargo = Cargo.objects.filter(email=user_obj.email).first()
        input_req = request.get_json()
        source = input_req['source']
        destination = input_req['destination']
        curr_cargo = cargo.names[name]

        curr_cargo['source'] = source
        curr_cargo['destination'] = destination
        cargo.names[name] = curr_cargo
        cargo.save()

        res = []
        for i in cargo.names:
            res.append({i: cargo.names[i]})

        try:
            api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + source + '&destination=' + destination + '&key=' + "api_key"
            response = requests.get(api_url)
            json_data = json.loads(response.text)
            if not json_data['routes'][0]:
                return jsonify({"result": True, "message": "No route exists between source and destination"})

            steps = json_data['routes'][0]['overview_polyline']['points']
            steps = polyline.decode(steps)
            return jsonify({"result": True, "data": {"locations": steps}})

        except:
            return jsonify({"result": True, "message": "Cannot connect to Google Maps"})



@users_blueprint.route('/updatesensor/<cargoname>', methods=["POST"])
@login_required
def updatesensor(cargoname=None):
    if request.method == "POST":
        user_obj = current_user
        input_req = request.get_json()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})
        cargo = Cargo.objects.filter(email=user_obj.email).first()
        cargo_obj = cargo["cargos"][cargoname]
        if not cargo_obj:
            return jsonify({"result": False, "message": "cargo with given name does not exist"})

        value = randint(24, 28)
        sensorid = cargo_obj['sensor_id']

        if not sensorid:
            return jsonify({"result": False, "message": "No sensor mapped to this cargo"})

        # sensor_obj = Sensor.objects.filter(email=user_obj.email, sensorid=sensorid).first()
        # print(sensor_obj['sensorid'])
        obj = {"time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "position": input_req["position"],
               "temperature": value}
        url = "http://***REMOVED***/mine"
        data={"time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "sensor_id": sensorid, "email":user_obj.email, 
                                        "position": input_req["position"], "temperature": value, "id": input_req['route_id'], "weight": value+5}
        resp = requests.post(url, data=data)
        # print(data)
        # print(resp)
        # sensor_obj.save()

        return jsonify({"result": True, "message": "Updated in blockchain!"})


@users_blueprint.route('mobile/updatesensor/<user_id>/<cargoname>', methods=["POST"])
@login_required
def mobile_updatesensor(user_id, cargoname=None):
    if request.method == "POST":
        user_obj = Users.objects.filter(user_id=user_id).first()

        input_req = request.get_json()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        cargo = Cargo.objects.filter(email=user_obj.email).first()
        cargo_obj = cargo["names"][cargoname]

        if not cargo_obj:
            return jsonify({"result": False, "message": "cargo with given name does not exist"})

        value = randint(24, 28)
        sensorid = cargo_obj['sensor']

        if not sensorid:
            return jsonify({"result": False, "message": "No sensor mapped to this cargo"})

        sensor_obj = Sensor.objects.filter(email=user_obj.email, sensorid=sensorid).first()
        print(sensor_obj['sensorid'])
        obj = {"time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "position": input_req["position"],
               "temperature": value}
        sensor_obj['locations'].append(obj)
        url = "http://***REMOVED***/mine"
        resp = requests.post(url, data={"time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                        "position": input_req["position"], "temperature": value, "id": sensor_obj.id})
        print(resp)
        sensor_obj.save()

        return jsonify({"result": True, "message": "Updated in database!"})
