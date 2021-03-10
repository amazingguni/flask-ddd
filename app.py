import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
config_object = os.environ.get('APP_SETTINGS', 'config.development.DevelopmentConfig')
app.config.from_object(config_object)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return 'Hello, World!'
from order.domain.order import Order

if __name__ == '__main__':
    app.run()
    

