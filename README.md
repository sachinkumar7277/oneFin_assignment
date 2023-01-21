# OneFin_assignment
OneFin assignment for building movie-collection api for web application with JWT authentication
# Project Set Up Installation
    run below command in your terminal 
    git clone https://github.com/sachinkumar7277/oneFin_assignment.git
    create and activate virtual environment
    1. python -m venv venv 
    2. venv/Scripts/activate
    Install all dependency or packages
    3.pip install -r requirements.txt

We are using python-decouple library to hide our confidential data 
please follow .env_sample file and create your own .env file
with all environment variable that is mentioned in .env_sample file

# For hiding your credentials we are using decouple library as shown below
    In settings.py
    from decouple import config
    SECRET_KEY = config('SECRET_KEY')

# create database in postgreSQL and configure the NAME with database name in .env file like
    NAME=onefin
    USER=postgres
    PASSWORD=your Database password here
    HOST=localhost
# For running the project execute below command in terminal
    create database in postgreSQL and configure the NAME with database name in .env file
    1. python manage.py makemigrations
    2. python manage.py migrate
    3. python manage.py runserver



