## Django boilerplate

## How to set up project

## How to run project locally bash script (Linux, Mac)

### install requirements

```bash
python3 -m venv env 
source env/bin/activate
pip install -r requirements/develop.text
```

### create .env file

```bash
cp .env.example .env
```

### create database

```bash
sudo -u postgres psql
CREATE DATABASE db_name;
\q
```

### set up .env file with your database credential

```bash
nano .env
```

### run migrations

```bash
python manage.py migrate
```

### run server

```bash
python manage.py runserver
```