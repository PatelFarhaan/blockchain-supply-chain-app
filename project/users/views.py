from common_utilities.cargo_json_schema import validate_user_cargo
from common_utilities.sensor_json_schema import validate_user_sensor
from project.models import Users, Warehouse, Cargo, Sensor
from flask_login import login_user, current_user, login_required, logout_user
from flask import Blueprint, request, jsonify
from project.users.users_serializer import UserSchema
from common_utilities.user_json_schema import user_login, user_register
from common_utilities.warehouse_json_schema import validate_user_warehouse
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import polyline
import json
from random import randint
from datetime import datetime

users_blueprint = Blueprint('user', __name__, url_prefix='/user')

api_key = ""

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
                cargo_obj_names = {input_req["name"]:{"source":"","destination": "", "sensor":""}}
                new_cargo_obj = Cargo(names=cargo_obj_names, email=email)
                new_cargo_obj.save()
                return jsonify({"result": True, "message": "cargo object created"})
            else:
                cargo_obj.names[input_req["name"]]={"source":"","destination": "", "sensor":""}
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
        for i in cargo_obj.names:
            res.append({i: cargo_obj.names[i]})

        return jsonify({"result": True, "data": res})

###############################

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
            if input_req['sensor_type'] == 'cargo':
                sensor_type = 'cargo'
                cargo = input_req['cargo']
                new_sensor_obj = Sensor(email=email, sensorid=str(Sensor.objects.count() + 1),cargo=cargo,locations={})
                new_sensor_obj.save()
                return jsonify({"result": True, "message": "sensor object created"})

            elif input_req['sensor_type'] == 'warehouse':
                sensor_type = 'warehouse'
                warehouse = input_req['warehouse']
                new_sensor_obj = Sensor(email=email, sensorid=str(Sensor.objects.count() + 1),warehouse=warehouse,locations={})
                new_sensor_obj.save()
                return jsonify({"result": True, "message": "sensor object created"})
            
            else:
                new_sensor_obj = Sensor(email=email,sensorid=str(Sensor.objects.count() + 1),locations={})
                new_sensor_obj.save()
                return jsonify({"result": True, "message": "sensor object created"})

        else:
            return jsonify(resp_obj)
    
    elif request.method == "PATCH":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})
        
        input_req = request.get_json()
        sensorid = input_req['sensorid']
        sensor_obj = Sensor.objects.filter(email=user_obj.email,sensorid=sensorid).first()

        if not sensor_obj:
            return jsonify({"result": False, "message": "No sensor found with this id"})

        for i in ('sensor_type','cargo','warehouse'):
            if i in input_req:
                if sensor_obj[i] != input_req[i]:
                    sensor_obj[i] = input_req[i]
        #Updated object
        sensor_obj.save() 

        if sensor_obj['sensor_type'] == "cargo":
            print("cargo name:::",sensor_obj['cargo'])
            cargo = Cargo.objects.filter(email=user_obj.email).first()
            cargo_obj = cargo["names"][sensor_obj['cargo']]
            print("CARGO OBJ:",cargo_obj)

            cargo_obj['sensor'] = sensorid
            cargo["names"][sensor_obj['cargo']] = cargo_obj
            cargo.save()


        return jsonify({"result": True, "data": sensor_obj})
        
    elif request.method == "GET":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})

        sensors = Sensor.objects.filter(email=user_obj.email).all()
        if not sensors:
            return jsonify({"result": False, "message": "No sensors found for this user"})

        res = sensors

        return jsonify({"result": True, "data": res})


##########################################



@users_blueprint.route('/cargo/<name>', methods=["POST"])
@login_required
def updatecargo(name=None):
    if not name:
        return jsonify({"result": False, "message": "Invalid cargo name"})
    
    if request.method == "POST":
        user_obj = current_user
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})
        cargo = Cargo.objects.filter(email=user_obj.email).first()

        input_req = request.get_json()
        source = input_req['source']
        destination = input_req['destination']
        # sensor = input_req['sensor']
        curr_cargo = cargo.names[name]

        curr_cargo['source'] = source
        curr_cargo['destination'] = destination
        # curr_cargo['sensor'] = sensor
        cargo.names[name] = curr_cargo
        cargo.save()

        res = []
        for i in cargo.names:
            res.append({i: cargo.names[i]})

        try:
            api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+source+'&destination='+destination+'&key=' + api_key
            response = requests.get(api_url)
            json_data = json.loads(response.text)
            if not json_data['routes'][0]:
                return jsonify({"result": True, "message": "No route exists between source and destination"})

            steps = json_data['routes'][0]['overview_polyline']['points']
            steps = polyline.decode(steps)
            return jsonify({"result": True, "data": {"locations": steps}})
           
        except:
            return jsonify({"result": True, "message": "Cannot connect to Google Maps"})
            
        


##########################################


@users_blueprint.route('/updatesensor/<cargoname>', methods=["POST"])
@login_required
def updatesensor(cargoname=None):
    if request.method == "POST":
        user_obj = current_user
        input_req = request.get_json()
        if not user_obj:
            return jsonify({"result": False, "message": "user does not exists"})
        print("CARGO NAME:",cargoname)
        cargo = Cargo.objects.filter(email=user_obj.email).first()
        cargo_obj = cargo["names"][cargoname]
        # print(cargo_obj)
        if not cargo_obj:
            return jsonify({"result": False, "message": "cargo with given name does not exist"})

        value = randint(24, 28)
        sensorid = cargo_obj['sensor']
        print("SENSOR NAME:",sensorid)

        if not sensorid:
            return jsonify({"result": False, "message": "No sensor mapped to this cargo"})

        sensor_obj = Sensor.objects.filter(email=user_obj.email,sensorid=sensorid).first()
        # print(sensor_obj['sensorid'],sensor_obj['locations'])
        sensor_obj['locations'].append({"time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "position":input_req["position"], "temperature":value})
        sensor_obj.save()

        return jsonify({"result": True, "message": "Updated in database!"})
