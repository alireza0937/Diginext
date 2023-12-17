#!/bin/sh
sleep 45

python manage.py makemigrations
python manage.py migrate


python run_python.py
