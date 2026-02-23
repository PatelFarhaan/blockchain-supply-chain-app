import enum


class CONSTANT(enum.Enum):
    SECRET_KEY = "***REMOVED***"
    PRIMARY_DB_CLUSTER = "mongodb://127.0.0.1:27017/admin"
    PORT = 80