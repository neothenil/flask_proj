import os
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor as TPE, as_completed

from . import celery, TaskExecutionError
from .utils import compress

default_nworker = os.cpu_count() // 2


@celery.task(bind=True)
def run_locust(self, hint):
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
    run_dir = Path(celery.conf.LOCUST_RUN_DIR, hint)
    run_dir.mkdir(exist_ok=True)
    input_path = Path(celery.conf.LOCUST_UPLOAD_DIR, hint + ".zip")
    try:
        with ZipFile(input_path) as zipfile:
            zipfile.extractall(path=run_dir)
    except Exception as e:
        meta["status"] = "FAILURE"
        return meta
    # run locust in workspace
    cwd = os.getcwd()
    os.chdir(run_dir)
    workspaces = []
    for direntry in os.scandir():
        if direntry.is_dir():
            workspaces.append(direntry.name)
    if not workspaces:
        meta["status"] = "FAILURE"
        return meta
    meta["status"] = "STARTED"
    meta["total"] = len(workspaces)
    self.update_state(state="STARTED", meta=meta)
    for info in async_execute_locust(
        celery.conf.LOCUST_BIN, workspaces, default_nworker
    ):
        meta.update(info)
        self.update_state(state="STARTED", meta=meta)
    # collect result to a zip file
    dl_path = Path(celery.conf.LOCUST_DOWNLOAD_DIR, hint + ".zip")
    zipfile = compress(dl_path, ".")
    os.chdir(cwd)
    shutil.rmtree(run_dir, ignore_errors=True)
    # return final status
    if len(meta["failed"]) != 0:
        meta["status"] = "FAILURE"
    else:
        meta["status"] = "SUCCESS"
    return meta


def execute_locust(locust_bin, workspace):
    all_files = os.listdir(workspace)
    xml_files = list(filter(lambda file: file.endswith(".xml"), all_files))
    if len(xml_files) != 1:
        raise FileNotFoundError(
            f"can not determine the input file for `{workspace}`"
        )
    input_file = xml_files[0]
    locust_bin = os.path.abspath(locust_bin)
    command = [locust_bin, input_file]
    subprocess.run(command, cwd=workspace, check=True)


def async_execute_locust(locust_bin, workspaces, nworker):
    total = len(workspaces)
    worker_num = min(total, nworker, os.cpu_count())
    if worker_num <= 0:
        return
    info = {"total": total, "success": 0, "failed": []}
    with TPE(max_workers=worker_num) as executor:
        futures = {
            executor.submit(execute_locust, locust_bin, workspace): workspace
            for workspace in workspaces
        }
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                info["failed"].append(futures[future])
            else:
                info["success"] += 1
            yield info
