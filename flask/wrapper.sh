#!/bin/bash

# turn on bash's job control
set -m

# Start the flask app in the background
# development server
# python app.py &
# gunicorn server
gunicorn --workers=2 --timeout=1800 --threads=2 --worker-class=gthread -b 0.0.0.0:5000 wsgi &

# Start the celery worker
celery -A app.celery worker --loglevel=info --concurrency=2 -n worker1@h% & 
celery -A app.celery worker --loglevel=info --concurrency=2 -n worker2@h% &
celery -A app.celery worker --loglevel=info --concurrency=2 -n worker3@h% &

# Start Flower
celery -A app.celery flower