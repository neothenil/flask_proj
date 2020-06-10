import os
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile

from . import celery
from .utils import compress


@celery.task(bind=True)
def run_spark(self, hint):
    # init meta data
    meta = {
        "status": "PENDING",
        "pid": os.getpid(),
        "success": 0,
        "total": 1,
        "failed": [],
    }
    self.update_state(state="PENDING", meta=meta)
    # create workspace
    run_dir = Path(celery.conf.SPARK_RUN_DIR, hint)
    run_dir.mkdir(exist_ok=True)
    input_path = Path(celery.conf.SPARK_UPLOAD_DIR, hint + ".zip")
    try:
        with ZipFile(input_path) as zipfile:
            zipfile.extractall(path=run_dir)
    except Exception as e:
        meta["status"] = "FAILURE"
        return meta
    # run spark in workspace
    cwd = os.getcwd()
    os.chdir(run_dir)
    workspaces = []
    for direntry in os.scandir():
        if direntry.is_dir() and "spark.inp" in os.listdir(direntry.path):
            workspaces.append(Path(direntry.path).resolve())
    if not workspaces:
        meta["status"] = "FAILURE"
        return meta
    workspaces.sort()  # sort the workspaces in alphabetical order
    meta["status"] = "STARTED"
    meta["total"] = len(workspaces)
    self.update_state(state="STARTED", meta=meta)
    for workspace in workspaces:
        try:
            subprocess.run([celery.conf.SPARK_BIN], cwd=workspace, check=True)
        except Exception:
            meta["failed"].append(workspace.name)
            self.update_state(state="STARTED", meta=meta)
            break
        else:
            meta["success"] += 1
            self.update_state(state="STARTED", meta=meta)
    # collect result to a zip file
    dl_path = Path(celery.conf.SPARK_DOWNLOAD_DIR, hint + ".zip")
    zipfile = compress(dl_path, ".")
    os.chdir(cwd)
    shutil.rmtree(run_dir, ignore_errors=True)
    # return final status
    if len(meta["failed"]) != 0:
        meta["status"] = "FAILURE"
    else:
        meta["status"] = "SUCCESS"
    return meta
