from flask import Blueprint

task_bp = Blueprint('task', __name__, url_prefix='/task')


@task_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    return 'submit page'


@task_bp.route('/<int:task_id>/download', methods=['GET'])
def download(task_id):
    return 'download page'


@task_bp.route('/<int:task_id>/delete', methods=['GET'])
def delete(task_id):
    return 'delete page'


@task_bp.route('/<int:task_id>/cancel', methods=['POST'])
def cancel(task_id):
    return 'cancel page'
