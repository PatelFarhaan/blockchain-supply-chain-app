from project import ma


class AdminSchema(ma.Schema):
    class Meta:
        fields = ("first_name", "last_name", "email", "is_admin")


class UserObj(ma.Schema):
    class Meta:
        fields = ("user_id", "first_name", "last_name", "email")