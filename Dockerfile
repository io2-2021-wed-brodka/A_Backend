FROM ubuntu

# install required packages
RUN apt update \
    && apt install -y git python3 python3-venv python3-pip

# setup the project
WORKDIR /bikes_server
COPY . /bikes_server/
RUN python3 -m venv venv \
    && venv/bin/pip3 install -r requirements.txt \
    && export BIKES_SQLITE=1 \
    && venv/bin/python3 manage.py makemigrations \
    && venv/bin/python3 manage.py migrate --run-syncdb \
    && venv/bin/python3 manage.py runscript docker_setup
