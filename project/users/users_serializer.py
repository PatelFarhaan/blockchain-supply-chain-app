from project import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ("first_name", "last_name", "email")


class UserMobileSchema(ma.Schema):
    class Meta:
        fields = ("first_name", "last_name", "email", "id")


class UserCargo(ma.Schema):
    class Meta:
        fields = ( "name", "source", "sensor_id", "driver_age", "driver_name", "destination", "email", "cargo_registration", "source_warehouse_id", "driver_license_number", "destination_warehouse_id", "created")