from uvicorn.workers import UvicornWorker

bind = '0.0.0.0:8000'
workers = 1
worker_class = UvicornWorker

timeout = 5
daemon = False

reload = True  # for dev only
# # preload = True  # Default: False (incompatible with reload=true)
# # Load application code before the worker processes are forked.
# # By preloading an application you can save some RAM resources as well as speed up server boot times.

# 2023-01-09T10:48:21+0100 200 GET /admin/ 1.377518s
access_log_format = (
    '%(T)s '  # 2023-01-09T10:48:21+0100 - date of the request in ISO format
    '%(s)s '  # 200 - status
    '%(m)s '  # GET - request method
    '%(U)s '  # /admin/ - URL path without query string
    '%(L)ss'  # 1.377518s - request time in decimal seconds
)
accesslog = '-'
errorlog = '-'
loglevel = 'debug'
capture_output = True  # Redirect stdout/stderr to Error log.
enable_stdio_inheritance = True  # Enable inheritance for stdio file descriptors in daemon mode.
