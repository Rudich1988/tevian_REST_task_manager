from flask import Flask

from task_manager.config.base import Config


app = Flask(__name__)
app.config.from_object(Config)


from task_manager.routes.tasks_routes import *
from task_manager.routes.faces_routes import *
from task_manager.routes.images_routes import *


app.register_blueprint(tasks_bp)
app.register_blueprint(images_bp)
app.register_blueprint(faces_bp)