import os
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)
