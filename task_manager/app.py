from flask import Flask
from flask_httpauth import HTTPBasicAuth

from task_manager.config.base import Config


app = Flask(__name__)
app.config.from_object(Config)

auth = HTTPBasicAuth()

USER = Config.EMAIL_NAME
PASSWORD = Config.EMAIL_PASSWORD


@auth.verify_password
def verify_password(username, password):
    if username == USER and password == PASSWORD:
        return username
    return None


from task_manager.routes.tasks_routes import *
from task_manager.routes.faces_routes import *
from task_manager.routes.images_routes import *


app.register_blueprint(tasks_bp)
app.register_blueprint(images_bp)
#app.register_blueprint(faces_bp)
