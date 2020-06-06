import os
from concurrent.futures import ThreadPoolExecutor as TPE, as_completed

from . import celery


@celery.task(bind=True)
def run_locust(self, task_id):
    # create workspace
    # run locust in workspace
    # collect result to a zip file
    pass


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
