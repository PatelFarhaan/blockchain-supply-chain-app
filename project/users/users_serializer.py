from project import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ("first_name", "last_name", "email")