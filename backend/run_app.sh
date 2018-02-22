#!/bin/sh

# wait for Postgresql server to start
sleep 4

# prepare init migration
su -m user -c "python manage.py makemigrations"
# migrate db, so we have the latest db schema
su -m user -c "python manage.py migrate"
# start development server on public ip interface, on port 8000
su -m user -c "python manage.py runserver 0.0.0.0:8000"
