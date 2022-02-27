# Airflow

Airflow is a workflow management system utilizing Directed Acyclic Graphs (DAGS) to connect various tasks together. Main advantage of using Airflow is writing the tasks in python scripts which can be deployed easily by uploading them to the Airflow. 

In this project, Airflow manages two data sources: reviews of books scrapped from [goodreads](www.goodreads.com) and Segment API that generates website visits.

# Development and Production Level Setup

For local development and test, we can use development setup and for operational processes airflow can be deployed to a cloud machine or VPS.

## Development

Development setup is in the local machine. For local development, we need to export all environment variables in `.env` file. Following shell script exports all (one should note that this approach doesn't work with variables who has spaces):

```sh
#!/bin/sh
#source this file
export $(xargs < .env)
```

Run `source export_env` before installing airflow.

This setup assumes Ubuntu based linux system. Setup a MySQL backend for meta-database with a database client.

```sql
CREATE DATABASE airflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'airflow_user' IDENTIFIED BY 'airflow_pass';
GRANT ALL PRIVILEGES ON airflow_db.* TO 'airflow_user';
```

Add database MySQL URI as environment variable to `.env` file as 

```bash
AIRFLOW__CORE__SQL_ALCHEMY_CONN=+mysqlconnector://airflow_user:airflow_pass@<database_url>:3306/airflow_db
```

Source the environmental variables with following command:

```bash
$ source export_env.sh
```

And then install all the requirements with pip:

```bash
$ pip install -r requirements.txt
```

Now, we need to create a user:

```bash
$ airflow users create \
    --username admin \
    --firstname onur \
    --lastname tunali \
    --role Admin \
    --email <email>
    -- password <password>
```

and finally initialize database:

```bash
airflow db init
```

## Production

Production setup is the same as development, however it's in Heroku PaaS. Heroku provides `DATABASE_URI` environment variable for a free tier PostgreSql database back-end. This needs to be copied to `AIRFLOW__CORE__SQL_ALCHEMY_CONN` secret in Heroku dashboard if one chooses to use that database.

As a side note, Heroku bash shell is ephemeral meaning when connected with 

```bash
heroku run bash --app erbap
```
every change or data created will be erased or rollbacked immediately after log out. That's why `Procfile` needs an initialization command with `release: airflow db init` before running the server using `web: airflow webserver --port $PORT --daemon & airflow scheduler`. In short `Procfile` should look lite this:

```sh
release: airflow db init
web: airflow webserver --port $PORT --daemon & airflow scheduler
```