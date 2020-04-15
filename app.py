from project import app
from common_utilities import CONSTANT
from project import app, port


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)
