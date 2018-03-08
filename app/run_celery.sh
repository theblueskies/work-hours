#!/bin/sh

# wait for Redis server to start
sleep 4

# run Celery worker
su -m user -c "celery worker -A payroll.celeryconf --loglevel=info"
