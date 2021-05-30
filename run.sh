#!/bin/bash

venv/bin/python3 manage.py runjobs minutely
venv/bin/gunicorn -b 0.0.0.0:8080 A_Backend.wsgi
