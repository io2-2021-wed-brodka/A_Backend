FROM python:3

# install cron
RUN apt update \
    && apt install -y cron

WORKDIR /bikes_server
COPY . /bikes_server/
RUN chmod +x run.sh

# setup project environment
RUN python3 -m venv venv \
    && venv/bin/pip3 install -r requirements.txt \
    && export BIKES_SQLITE=1 \
    && venv/bin/python3 manage.py makemigrations \
    && venv/bin/python3 manage.py migrate --run-syncdb \
    && venv/bin/python3 manage.py runscript test_db_setup --script-args api_test_setup/stations.json api_test_setup/bikes.json \
    && echo '* * * * * cd /bikes_server && export BIKES_SQLITE=1 && venv/bin/python3 manage.py runjobs minutely' | crontab
