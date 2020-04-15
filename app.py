from project import app
from common_utilities import CONSTANT


if __name__ == '__main__':
    app.run(debug=True, port=CONSTANT.PORT.value)