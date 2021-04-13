# A_Backend

## Project setup

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
