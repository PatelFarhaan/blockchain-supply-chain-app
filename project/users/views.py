import json
import requests
import polyline
from random import randint
from datetime import datetime
from project import api_key, port
from common_utilities.wallet import Wallet
from common_utilities.blockchain import Blockchain
from project.users.users_serializer import UserSchema
from project.models import Users, Warehouse, Cargo, Sensor
from flask import Blueprint, request, jsonify, send_from_directory
from common_utilities.cargo_json_schema import validate_user_cargo
from common_utilities.sensor_json_schema import validate_user_sensor
from common_utilities.user_json_schema import user_login, user_register
from werkzeug.security import generate_password_hash, check_password_hash
from common_utilities.warehouse_json_schema import validate_user_warehouse
from flask_login import login_user, current_user, login_required, logout_user


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
    logout_user()
    return jsonify({"result":True, "message": "user logged out"})


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
                cargo_obj_names = {input_req["name"]: {"source": "", "destination": "", "sensor": ""}}
                new_cargo_obj = Cargo(names=cargo_obj_names, email=email)
                new_cargo_obj.save()
                return jsonify({"result": True, "message": "cargo object created"})
            else:
                cargo_obj.names[input_req["name"]] = {"source": "", "destination": "", "sensor": ""}
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
                locations = input_req["locations"]
                new_sensor_obj = Sensor(email=email, sensorid=str(Sensor.objects.count() + 1), cargo=cargo,
                                        locations=locations)
                new_sensor_obj.save()
                return jsonify({"result": True, "message": "sensor object created"})

            elif input_req['sensor_type'] == 'warehouse':
                sensor_type = 'warehouse'
                warehouse = input_req['warehouse']
                locations = input_req["locations"]
                new_sensor_obj = Sensor(email=email, sensorid=str(Sensor.objects.count() + 1), warehouse=warehouse,
                                        locations=locations)
                new_sensor_obj.save()
                return jsonify({"result": True, "message": "sensor object created"})

            else:
                new_sensor_obj = Sensor(email=email, sensorid=str(Sensor.objects.count() + 1), locations=[])
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
        sensor_obj = Sensor.objects.filter(email=user_obj.email, sensorid=sensorid).first()

        if not sensor_obj:
            return jsonify({"result": False, "message": "No sensor found with this id"})

        for i in ('sensor_type', 'cargo', 'warehouse'):
            if i in input_req:
                if sensor_obj[i] != input_req[i]:
                    sensor_obj[i] = input_req[i]
        # Updated object
        sensor_obj.save()

        if sensor_obj['sensor_type'] == "cargo":
            print("cargo name:::", sensor_obj['cargo'])
            cargo = Cargo.objects.filter(email=user_obj.email).first()
            cargo_obj = cargo["names"][sensor_obj['cargo']]
            print("CARGO OBJ:", cargo_obj)

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
        cargo.names[name] = curr_cargo
        cargo.save()

        res = []
        for i in cargo.names:
            res.append({i: cargo.names[i]})

        try:
            api_url = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + source + '&destination=' + destination + '&key=' + api_key
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
        print("CARGO NAME:", cargoname)
        cargo = Cargo.objects.filter(email=user_obj.email).first()
        cargo_obj = cargo["names"][cargoname]
        # print(cargo_obj)
        if not cargo_obj:
            return jsonify({"result": False, "message": "cargo with given name does not exist"})

        value = randint(24, 28)
        sensorid = cargo_obj['sensor']
        print("SENSOR NAME:", sensorid)

        if not sensorid:
            return jsonify({"result": False, "message": "No sensor mapped to this cargo"})

        sensor_obj = Sensor.objects.filter(email=user_obj.email, sensorid=sensorid).first()
        # print(sensor_obj['sensorid'],sensor_obj['locations'])
        sensor_obj['locations'].append(
            {"time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "position": input_req["position"],
             "temperature": value})
        sensor_obj.save()

        return jsonify({"result": True, "message": "Updated in database!"})




########################################################################################################################
############################################   :=> BLOCHCHAIN <=:   ####################################################
########################################################################################################################
@users_blueprint.route('/wallet', methods=['POST'])
def create_keys():
    wallet = Wallet(port)
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Saving the keys failed.'
        }
        return jsonify(response), 500


@users_blueprint.route('/wallet', methods=['GET'])
def load_keys():
    wallet = Wallet(port)
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Loading the keys failed.'
        }
        return jsonify(response), 500


@users_blueprint.route('/balance', methods=['GET'])
def get_balance():
    wallet = Wallet(port)
    balance = blockchain.get_balance()
    if balance is not None:
        response = {
            'message': 'Fetched balance successfully.',
            'funds': balance
        }
        return jsonify(response), 200
    else:
        response = {
            'messsage': 'Loading balance failed.',
            'wallet_set_up': wallet.public_key is not None
        }
        return jsonify(response), 500


@users_blueprint.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {'message': 'No data found.'}
        return jsonify(response), 400
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(key in values for key in required):
        response = {'message': 'Some data is missing.'}
        return jsonify(response), 400
    success = blockchain.add_transaction(
        values['recipient'],
        values['sender'],
        values['signature'],
        values['amount'],
        is_receiving=True)
    if success:
        response = {
            'message': 'Successfully added transaction.',
            'transaction': {
                'sender': values['sender'],
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': values['signature']
            }
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed.'
        }
        return jsonify(response), 500


@users_blueprint.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {'message': 'No data found.'}
        return jsonify(response), 400
    if 'block' not in values:
        response = {'message': 'Some data is missing.'}
        return jsonify(response), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message': 'Block added'}
            return jsonify(response), 201
        else:
            response = {'message': 'Block seems invalid.'}
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
        response = {
            'message': 'Blockchain seems to differ from local blockchain.'}
        blockchain.resolve_conflicts = True
        return jsonify(response), 200
    else:
        response = {
            'message': 'Blockchain seems to be shorter, block not added'}
        return jsonify(response), 409


@users_blueprint.route('/transaction', methods=['POST'])
def add_transaction():
    wallet = Wallet(port)
    if wallet.public_key is None:
        response = {
            'message': 'No wallet set up.'
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing.'
        }
        return jsonify(response), 400
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(
        recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            'message': 'Successfully added transaction.',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed.'
        }
        return jsonify(response), 500


@users_blueprint.route('/mine', methods=['POST'])
def mine():
    wallet = Wallet(port)
    if blockchain.resolve_conflicts:
        response = {'message': 'Resolve conflicts first, block not added!'}
        return jsonify(response), 409
    block = blockchain.mine_block()
    if block is not None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Block added successfully.',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a block failed.',
            'wallet_set_up': wallet.public_key is not None
        }
        return jsonify(response), 500


@users_blueprint.route('/resolve-conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {'message': 'Chain was replaced!'}
    else:
        response = {'message': 'Local chain kept!'}
    return jsonify(response), 200


@users_blueprint.route('/transactions', methods=['GET'])
def get_open_transaction():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200


@users_blueprint.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_chain), 200


@users_blueprint.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data attached.'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            'message': 'No node data found.'
        }
        return jsonify(response), 400
    node = values['node']
    blockchain.add_peer_node(node)
    response = {
        'message': 'Node added successfully.',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201


@users_blueprint.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url is None:
        response = {
            'message': 'No node found.'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node removed',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


@users_blueprint.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        'all_nodes': nodes
    }
    return jsonify(response), 200