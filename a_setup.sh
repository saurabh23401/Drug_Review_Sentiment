#!/bin/bash

# Set AIRFLOW_HOME directory
export AIRFLOW_HOME=./

# Initialize the Airflow database
airflow db init

# Create an Airflow admin user
airflow users create \
    --username admin \
    --firstname FIRST_NAME \
    --lastname LAST_NAME \
    --role Admin \
    --email your@email.com \
    --password adminpassword

echo "Airflow setup complete! Start the webserver and scheduler in separate terminals."
