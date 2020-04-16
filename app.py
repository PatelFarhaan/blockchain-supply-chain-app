from project import app
from common_utilities import CONSTANT


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CONSTANT.PORT.value, debug=True, use_reloader=True)
