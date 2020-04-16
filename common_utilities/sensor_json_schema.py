from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

######################################################################################################
users_sensor_schema = {
    "type": "object",
    "properties": {
        "sensorid": {
            "type": "string"
        },
        "sensor_type": {
            "type": "string"
        },
        "cargo": {
            "type": "string"
        },
        "warehouse": {
            "type": "string"
        },
        "locations": {
            "type": "array"
        }
    },
    "required": ["sensor_type"],
    "additionalProperties": False
}


def validate_user_sensor(data):
    try:
        validate(instance=data, schema=users_sensor_schema)
    except ValidationError as e:
        return {"result": False, "message": e.message}
    except SchemaError as e:
        return {"result": False, "message": e.message}
    return {"result": True, "data": data}

######################################################################################################
