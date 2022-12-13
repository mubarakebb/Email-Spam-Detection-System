web: gunicorn NewProject.wsgi --log-file -

web: gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:6958 --timeout 600
