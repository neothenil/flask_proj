from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from ..forms import TaskForm

task_bp = Blueprint("task", __name__, url_prefix="/task")


@task_bp.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    form = TaskForm()
    if form.validate_on_submit():
        flash("Submit task successfully!")
        return redirect(url_for("index"))
    return render_template("submit.html", form=form)


@task_bp.route("/<int:task_id>/download", methods=["GET"])
@login_required
def download(task_id):
    return "download page"


@task_bp.route("/<int:task_id>/delete", methods=["GET"])
@login_required
def delete(task_id):
    return "delete page"


@task_bp.route("/<int:task_id>/cancel", methods=["POST"])
@login_required
def cancel(task_id):
    return "cancel page"
