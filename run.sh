#!/bin/bash

cron
venv/bin/gunicorn -b 0.0.0.0:8080 A_Backend.wsgi
