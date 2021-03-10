from flask import Flask, request, Response

from config import RUNNING_ADDRESS, PORT

from database.db import initialize_db
import logging

from modules.money import money as money_api
from modules.places import places as places_api
from modules.user import user as user_api

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'LifeBot',
    'host': 'mongodb+srv://root:root@cluster0.ro0oy.mongodb.net/test'
}

initialize_db(app)

app.register_blueprint(money_api)
app.register_blueprint(places_api)
app.register_blueprint(user_api)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@app.route('/')
def hello_world():
    return 'Moe Flask приложение в контейнере Docker.'


if __name__ == '__main__':
    app.run(threaded=True, debug=True, host=RUNNING_ADDRESS, port=PORT)
