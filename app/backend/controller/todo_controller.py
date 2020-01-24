import logging
import sys

from flask import Blueprint, jsonify

from app.backend.model.todo import Todo
from app.backend.model.todo_controller import TodoController
from app.backend.service.mongo_db_connector_service import MongoDBConnectorService

todo_blueprint = Blueprint('todo', __name__, url_prefix='/todo')
todo_controller = TodoController(MongoDBConnectorService())

log = logging.getLogger(__name__)
# Temporary logging stdout for class debugging
if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler(sys.stdout))


@todo_blueprint.route('/get_task_list')
def get_task_list():
    log.debug("client request for task list.")
    task_list = [task.to_dict() for task in todo_controller.find_all()]
    return jsonify(task_list), 200, {'ContentType': 'application/json'}


@todo_blueprint.route('/add_task/<todo_title>', methods=['GET'])
def add_task(todo_title):
    log.debug(f"client request adding task: {todo_title}")
    try:
        inserted_result = todo_controller.insert_one(Todo(todo_title))
    except Exception as err:
        log.exception(err)
        return jsonify({"success": False, "msg": "Exception: [{}] {}".format(type(err).__name__, str(err))}), 500, {
            'ContentType': 'application/json'}
    return jsonify({"success": True, "job_id": str(inserted_result.inserted_id)}), 200, {
        'ContentType': 'application/json'}
