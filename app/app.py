import logging

from flask import Flask

from app.config_loader import AppConfig
from app.logger_loader import LoggerLoader
from app.backend.controller.landing_controller import landing_blueprint
from app.backend.controller.todo_controller import todo_blueprint
from app.backend.util.custom_json_decoder import get_custom_json_decoder
from app.backend.util.custom_json_encoder import get_custom_json_encoder

LoggerLoader()
app = Flask(__name__)
app_config: AppConfig = AppConfig()
app.json_decoder = get_custom_json_decoder(app_config)
app.json_encoder = get_custom_json_encoder(app_config)
app.register_blueprint(landing_blueprint)
app.register_blueprint(todo_blueprint)

if __name__ == '__main__':
    app.run(host=AppConfig().config["FLASK_RUNNING_IP"], port=AppConfig().config["FLASK_RUNNING_PORT"], threaded=True,
            debug=AppConfig().config["FLASK_ENABLE_DEBUGGING"])
