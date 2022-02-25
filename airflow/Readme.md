# Airflow

Airflow is a workflow management system utilizing Directed Acyclic Graphs (DAGS) to connect various tasks together. Main advantage of using Airflow is writing the tasks in python scripts which can be deployed easily by uploading them to the Airflow. 

In this project, Airflow manages two data sources: reviews of books scrapped from goodreads.com and Segment api that generates website visits.

# Setup 

We have two different setups, development and production.

## Development

Development setup is in the local machine. For local development, we need to export all environment variables in `.env` file. Following shell script exports all (one should note that this approach doesn't work with variables who has spaces):

```sh
#!/bin/sh
#source this file
export $(xargs < .env)
```

Run `source export_env` before installing airflow.


## Production

Production setup is in Heroku PaaS. New version of SQLAlchemy uses `postgresql` instead of `postgres` in database URI and Heroku stills uses the first version in free tier PostgresSql database example. That's why there are some conflict with dependencies. After installing airflow, following libraries should be anchored to previous version in `requirement.txt`:

```
SQLAlchemy==1.3.24
MarkupSafe==2.0.1
```

In addition, Heroku provide `DATABASE_URI` environment variable and this needs to be copied to `AIRFLOW__CORE__SQL_ALCHEMY_CONN` secret in Heroku dashboard.


As a side note, Heroku bash shell is ephemeral meaning when connected with 

```bash
heroku run bash --app erbap
```
every change or data created will be erased or rollbacked immediately after log out. That's why `Procfile` needs an initialization command with `release: airflow db init` before running the server using `web: airflow webserver --port $PORT --daemon & airflow scheduler`. In short `Procfile` should look lite this:

```sh
release: airflow db init
web: airflow webserver --port $PORT --daemon & airflow scheduler
```