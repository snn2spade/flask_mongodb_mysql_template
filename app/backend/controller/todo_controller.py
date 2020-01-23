import logging
import sys

from flask import Blueprint, jsonify

from app.backend.model.job import Job
from app.backend.model.job_controller import JobController
from app.backend.service.mongo_db_connector_service import MongoDBConnectorService

todo_blueprint = Blueprint('todo', __name__, url_prefix='/todo')
job_controller = JobController(MongoDBConnectorService())

log = logging.getLogger('app.' + __name__)
# Temporary logging stdout for class debugging
if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler(sys.stdout))


@todo_blueprint.route('/get_job_list')
def get_job_list():
    log.info("client request for job list.")
    job_list = [job.to_dict() for job in job_controller.find_all()]
    return jsonify(job_list), 200, {'ContentType': 'application/json'}


@todo_blueprint.route('/add_job/<job_title>', methods=['GET'])
def add_job(job_title):
    log.info(f"client request adding job: {job_title}")
    try:
        inserted_result = job_controller.insert_one(Job(job_title))
    except Exception as err:
        log.exception(err)
        return jsonify({"success": False, "msg": "Exception: [{}] {}".format(type(err).__name__, str(err))}), 500, {
            'ContentType': 'application/json'}
    return jsonify({"success": True, "job_id": str(inserted_result.inserted_id)}), 200, {
        'ContentType': 'application/json'}
