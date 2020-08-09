class Job:
    """Job object for worker threads."""
    def __init__(self, job_type, body, creator_type, worker_type):
        self.job_type = job_type
        self.body = body
        self.creator_type = creator_type
        self.worker_type = worker_type
