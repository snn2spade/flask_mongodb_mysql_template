import logging
import subprocess

from flask import Flask, jsonify

from ConfigLoader import AppConfig
from LoggerLoader import LoggerLoader
from backend.CustomJSONDecoder import CustomJSONDecoder
from backend.CustomJSONEncoder import CustomJSONEncoder
from backend.MongoDBConnectorService import MongoDBConnectorService
from backend.model.mongo.Job import Job
from backend.model.mongo.JobController import JobController

app = Flask(__name__)
log = logging.getLogger('app.' + __name__)
app.json_decoder = CustomJSONDecoder
app.json_encoder = CustomJSONEncoder
app_config: AppConfig = AppConfig()


# APP SERVICE INFO
def get_git_revision():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
    except subprocess.CalledProcessError:
        return None


def get_git_tag():
    try:
        return subprocess.check_output(["git", "describe"]).strip().decode("utf-8")
    except subprocess.CalledProcessError:
        return None


def get_service_info():
    return {"revision": get_git_revision(), "tag": get_git_tag(), "service_name": app_config.config["APP_NAME"]}


# API ROUTE
@app.route('/get_job_list')
def get_job_list():
    job_list = [job.to_dict() for job in job_controller.find_all()]
    return jsonify(job_list), 200, {'ContentType': 'application/json'}


@app.route('/add_job/<job_title>', methods=['GET'])
def add_job(job_title):
    try:
        inserted_result = job_controller.insert_one(Job(job_title))
    except Exception as err:
        log.exception(err)
        return jsonify({"success": False, "msg": "Exception: [{}] {}".format(type(err).__name__, str(err))}), 500, {'ContentType': 'application/json'}
    return jsonify({"success": True, "job_id": str(inserted_result.inserted_id)}), 200, {'ContentType': 'application/json'}


@app.route('/info', methods=['GET'])
def get_service_info_api():
    return jsonify({"api_info": get_service_info()})


if __name__ == '__main__':
    # Load Logging config
    LoggerLoader()
    log.info("<-------------- START SERVER --------------->")

    job_controller = JobController(MongoDBConnectorService())

    app.run(host=AppConfig().config["FLASK_RUNNING_IP"], port=AppConfig().config["FLASK_RUNNING_PORT"], threaded=True,
            debug=AppConfig().config["FLASK_ENABLE_DEBUGGING"])
