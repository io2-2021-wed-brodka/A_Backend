# A_Backend

## Project setup

### Run with `docker-compose`

From the project root directory run the command

```shell
docker-compose up
```

The container will be created and started automatically. The server will be accessible on `localhost:8080`. There will
already be an `Admin` created with credentials:

**username:** admin\
**password:** admin

### Local setup

1. After cloning repository, `cd` into it and run `python -m venv venv`.
2. When the virtual environment is created, install required packages:
    * Linux

      ```shell
      venv/bin/pip3 install -r requirements.txt
      ```
    * Windows

      ```shell
      venv/Scripts/pip3.exe install -r requirements.txt
      ```

3. Run Django migrations to create database.

   ```
   <venv python> manage.py makemigrations
   <venv python> manage.py migrate
   ```

### API tests setup

Create JSON files with stations and bikes to insert to DB before tests and run

```
python manage.py createsuperuser --username=admin --email=admin@bikes.com
python manage.py runscript test_db_setup --script-args api_test_setup/stations.json api_test_setup/bikes.json
```
