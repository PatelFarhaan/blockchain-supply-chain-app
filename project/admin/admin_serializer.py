from project import ma


class AdminSchema(ma.Schema):
    class Meta:
        fields = ("first_name", "last_name", "email", "is_admin")
