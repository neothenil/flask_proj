import uuid
import psutil
from pathlib import Path
from flask import (
    request,
    abort,
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    current_app,
    send_file,
)
from flask_login import login_required, current_user

from ..forms import TaskForm
from ..models import Task
from ..extension import db
from ..tasks import run_locust, run_spark

task_bp = Blueprint("task", __name__, url_prefix="/task")


@task_bp.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    form = TaskForm()
    if form.validate_on_submit():
        type = form.type.data
        name = form.name.data
        zipfile = form.zipfile.data
        id = uuid.uuid4().hex
        upload_dir = current_app.config[type + "_UPLOAD_DIR"]
        zipfile.save(Path(upload_dir, id + ".zip"))
        task = start_task(type, name, id)
        task.user = current_user._get_current_object()
        db.session.add(task)
        ab.session.commit()
        flash(f"Task <{task.name}> has been submitted successfully!")
        return redirect(url_for("index"))
    return render_template("submit.html", form=form)


def start_task(type, name, id):
    if type == "LOCUST":
        result = run_locust.apply_async(id, task_id=id)
    elif type == "SPARK":
        result = run_spark.apply_async(id, task_id=id)
    else:
        abort(500)
    while result.info is None:
        time.sleep(current_app.config["POLL_INTERVAL"])
    info = result.info
    status = info["status"]
    pid = info["pid"]
    process = int(info["success"] / info["total"] * 100.0)
    task = Task(
        id=id, name=name, type=type, status=status, pid=pid, process=process
    )
    return task


def update_tasks(tasks):
    for task in tasks:
        if task.status == "SUCCESS" or task.status == "FAILURE":
            continue
        type = task.type
        id = task.id
        if type == "LOCUST":
            task_obj = run_locust
        elif type == "SPARK":
            task_obj = run_spark
        result = task_obj.AsyncResult(id)
        info = result.info
        task.status = info["status"]
        task.process = int(info["success"] / info["total"] * 100.0)
        if task.status == "SUCCESS" or task.status == "FAILURE":
            task.pid = None
            result.forget()
        db.session.add(task)
    db.session.commit()


@task_bp.route("/<task_id>/download", methods=["GET"])
@login_required
def download(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user.id != current_user.id:
        abort(404)
    if task.status != "SUCCESS" and task.status != "FAILURE":
        abort(404)
    download_dir = current_app.config[task.type + "_DOWNLOAD_DIR"]
    path = Path(download_dir, task_id + ".zip")
    if not path.exists():
        abort(404)
    return send_file(path)


@task_bp.route("/<task_id>/delete", methods=["POST"])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user.id != current_user.id:
        abort(404)
    if request.form["taskname"] != task.name:
        flash(f"Wrong task name detected!")
        return redirect(url_for("index"))
    if task.status != "SUCCESS" and task.status != "FAILURE":
        abort(404)
    upload_dir = current_app.config[task.type + "_UPLOAD_DIR"]
    # run_dir should be deleted after execution by task
    download_dir = current_app.config[task.type + "_DOWNLOAD_DIR"]
    upload_path = Path(upload_dir, task_id + ".zip")
    download_path = Path(download_dir, task_id + ".zip")
    upload_path.unlink(missing_ok=True)
    download_path.unlink(missing_ok=True)
    db.session.delete(task)
    db.session.commit()
    flash(f"Task <{task.name}> deleted!")
    return redirect(url_for("index"))


@task_bp.route("/<task_id>/cancel", methods=["POST"])
@login_required
def cancel(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user.id != current_user.id:
        abort(404)
    if request.form["taskname"] != task.name:
        flash(f"Wrong task name detected!")
        return redirect(url_for("index"))
    if task.status == "SUCCESS" or task.status == "FAILURE":
        abort(404)
    if task.type == "LOCUST":
        task_obj = run_locust
    elif task.type == "SPARK":
        task_obj = run_spark
    task_result = task_obj.AsyncResult(task.id)
    proc = psutil.Process(task.pid)
    chidren = proc.chidren(recursive=True)
    task_result.revoke(terminate=True)
    for child in children:
        child.terminate()
    task.status = "FAILURE"
    task.pid = None
    db.session.add(task)
    db.session.commit()
    flash(f"Task <{task.name}> has been cancelled!")
    return redirect(url_for("index"))
