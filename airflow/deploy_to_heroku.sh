#!/bin/sh
# heroku login first

# If .git is not present no error occurs
echo "=== Started Deploying... ==="

rm -rf .git 

# git repo
git init
git add .
git commit -m "temp commit"
heroku git:remote -a erbap-airflow # Hard coded, needs to be changed for each app
git push -f heroku main

rm -rf .git
echo "=== Finished Deploying... ==="


