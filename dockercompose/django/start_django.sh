#!/bin/bash
python tinyapp/manage.py makemigrations
python tinyapp/manage.py migrate
python tinyapp/manage.py runserver 0.0.0.0:8001