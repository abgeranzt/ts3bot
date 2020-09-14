# std
import os
import yaml

# local
from ts3bot.logger import get_logger
from ts3bot.query.parser import Parser
from ts3bot.threads.job import Job

class Worker:
    def __init__(self, queue, worker_id):
        self._cfg = self._load_cfg()
        self._worker_id = worker_type
        self._logger = get_logger(f"worker_{worker_id}")
        self._queue = queue

    # --- Public Methods ---
    def work(self):


    # --- Private Methods ---

    def _do_parsing(self, job):
        """Parse query output and add Job to queue."""
        # TODO HERE
        if job.job_type == "query_event":
            pass
        pass

    @staticmethod
    def _load_cfg():
        """Load config and return it as dict."""
        cfg_path = os.path.join("config", "local", "worker.yaml")
        with open(cfg_path, "r") as cfg_file:
            cfg = yaml.safe_load(cfg_file)
        return cfg[self._worker_id]
