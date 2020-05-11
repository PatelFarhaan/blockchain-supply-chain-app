from project import app
from project import app, port
from common_utilities import CONSTANT


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port, debug=True, use_reloader=True)
