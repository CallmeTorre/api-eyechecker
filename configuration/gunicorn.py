import multiprocessing

bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 3 + 1
timeout = 600
graceful_timeout = 40
accesslog = "-"
errorlog = "-"