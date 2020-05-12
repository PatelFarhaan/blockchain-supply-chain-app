from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

######################################################################################################
users_cargo_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
                },
        "source": {
                    "type": "string"
                },
        "sensor_id": {
                    "type": "string"
                },
        "driver_age": {
                    "type": "integer"
                },
        "driver_name": {
                    "type": "string"
                },
        "destination": {
                    "type": "string"
                },
        "email": {
                    "type": "string"
                },
        "cargo_registration": {
                    "type": "string"
                },
        "source_warehouse_id": {
                    "type": "string"
                },
        "driver_license": {
                    "type": "string"
                },
        "destination_warehouse_id": {
                    "type": "string"
                },
    },
    "required": ["name", "source", "sensor_id", "driver_age", "driver_name", "destination",
                 "cargo_registration", "source_warehouse_id", "driver_license", "destination_warehouse_id"],
    "additionalProperties": False
}


def validate_user_cargo(data):
    try:
        validate(instance=data, schema=users_cargo_schema)
    except ValidationError as e:
        return {"result": False, "message": e.message}
    except SchemaError as e:
        return {"result": False, "messgae": e.message}
    return {"result": True, "data": data}
######################################################################################################
