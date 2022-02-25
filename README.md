# Erbap

> Scifi book recommendation engine

Erbap is a distributed book recommendation engine in the genre of science fiction novels. With its substantial database and sophisticated machine learning powered recommendation system approach, it is able to pinpoint your next favorite book down to its literary tropes.

This is a very comprehensive data engineering project showcasing different technical skills such as API implementation, web scraping, data ingestion from multiple sources, task scheduling, database managing, data warehouse constructing etc.

**Note:** Subdirectories include different apps (web_app, data_infra etc.) deployed to different heroku remotes. First, subtree approach is considered for management however, since heroku storages are not exactly git repos and for this reason ad hoc deploying bash scripts are used:

```bash
#!/bin/sh
# chmod +x <filename> make the file executable
# heroku login first before running the script

echo "=== Started Deploying... ==="

# If .git is not present no error occurs
rm -rf .git 

# git repo
git init
git add .
git commit -m "temp commit"
heroku git:remote -a $1 # App name obtained from argument
git push -f heroku main

rm -rf .git
echo "=== Finished Deploying... ==="
```

For extensive documentation refer [here.](http://www.onurtunali.com/Erbap)

# Contents

- [Web App](#Website)
- [Data Sources](#Data-sources)
    - [User Data](#Data-sources)
    - [Scraping](#Data-sources)
- [Documentation](#Data-sources)


# Web App

Main app is run in Heroku PaaS which presents the recommendation engine and other user features. For back end cookiecutter flask template is used as a boilerplate code. Tech stack is as follows:


## Front-end:
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white) ![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)
## Back-end: 
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)
## Database: 
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

# Data Sources

There are 2 main data sources. User activities on the website and book reviews and ratings scraped through goodreads.com that are the most recent entries.

## User data

User activities are logged with `blank_technology` and send to the data lake.

## Scraping

For scraping `requests` and `BeautifulSoup` libraries used for trigger based python script

# Data Infrastructure

## Data Pipeline
## Pipeline Task Management
## Operational Database
## Data Lake
## Data Warehouse


# Documentation

Sphinx documentation tool is used. Generating automated docsting `sphinx-apidoc -f -M -o source ../Erbap` command is run. The option `-M` is for module first.  

# Database Connection 

For free tier AWS RDS instance security group needs to be changes for universal connection. Go to your console and find security group. From there find the tab for "edit inbound rules". We need to add an inbound rule for MySQL database which enables connection from everywhere: 0.0.0.0/0

# Errors

- If you are having problem with installing `flask-mysqldb` and using another version of python other than system default, you need to install specific python dev tools. For example, given that virtualenv using python3.8, run this command: `sudo apt install python3.8-dev`.

- Original data csv id start with 0. However, in our DDL we define `id` column with `AUTO_INCREMENT` constraint so when importing the file databases doesn't accept that. Therefore we need to start id values with 1 and change the data accordingly.

- `SQL Error [1452] [23000]: Cannot add or update a child row...` error occurs when importing data with a foreign key column that has a value not present in parent table.

