#!/bin/bash
set -e

# Start the celery worker
celery -A main.celery_app worker --loglevel=info -P solo &

# Start the gunicorn server (production) or debug server (development)
python -m main

#gunicorn --bind 0.0.0.0:8050 main:server