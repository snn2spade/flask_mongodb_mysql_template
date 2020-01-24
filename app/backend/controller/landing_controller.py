import logging
import subprocess
import sys

from flask import Blueprint, jsonify

from app.config_loader import AppConfig

landing_blueprint = Blueprint('landing', __name__, url_prefix='/')

log = logging.getLogger(__name__)
# Temporary logging stdout for class debugging
if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler(sys.stdout))


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
    return {"revision": get_git_revision(), "tag": get_git_tag(), "service_name": AppConfig().config["APP_NAME"]}


@landing_blueprint.route('/', methods=['GET'])
def landing():
    log.debug("Client request for landing page.")
    return jsonify({'error': 'Page not found.'}), 404, {'ContentType': 'application/json'}


@landing_blueprint.route('/info', methods=['GET'])
def info():
    log.debug("Client request for service info.")
    return jsonify(get_service_info()), 200, {'ContentType': 'application/json'}
