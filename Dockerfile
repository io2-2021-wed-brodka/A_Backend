FROM python:3

WORKDIR /bikes_server
COPY . /bikes_server/
RUN python3 -m venv venv \
    && venv/bin/pip3 install -r requirements.txt \
    && export BIKES_SQLITE=1 \
    && venv/bin/python3 manage.py makemigrations \
    && venv/bin/python3 manage.py migrate --run-syncdb \
    && venv/bin/python3 manage.py runscript test_db_setup --script-args api_test_setup/stations.json api_test_setup/bikes.json
