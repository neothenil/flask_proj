from flask import Blueprint, render_template, flash, redirect, url_for

from ..forms import TaskForm

task_bp = Blueprint('task', __name__, url_prefix='/task')


@task_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    form = TaskForm()
    if form.validate_on_submit():
        flash('Submit task successfully!')
        return redirect(url_for('index'))
    return render_template('submit.html', form=form)


@task_bp.route('/<int:task_id>/download', methods=['GET'])
def download(task_id):
    return 'download page'


@task_bp.route('/<int:task_id>/delete', methods=['GET'])
def delete(task_id):
    return 'delete page'


@task_bp.route('/<int:task_id>/cancel', methods=['POST'])
def cancel(task_id):
    return 'cancel page'
