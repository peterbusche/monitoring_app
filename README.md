# Name: 
    monitoring_app

# Summary: 
    This is a python app that when run, checks the endpoints of designated URLs and save read status code and timestamp of the check. This check is set to a scheduler, so it will continuously make these checks at a dynamic interval until the app is stopped. The information stored by this app is available via an exposed /metrics endpoint. This endpoint will give back a json that has a built in query for formatting. 


# Technologies Used:
    python 3.8+
    PostgreSQL 17.2 
    Discord

    Python Libraries:
        Flask
        SQLAlchemy
        requests
        APScheduler
        PyYAML
        psycopg2-binary
        

# Installation:
    Clone the Repository:
        git clone https://github.com/peterbusche/monitoring_app

    Set up VM and login (optional):
        python -m venv venv

    Install Dependencies:
        pip install -r requirements.txt

    Install PostgreSQL 17.2 and Login:
        https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

        psql -h localhost -U postgres -p 5432

    Create the database in psql terminal and connect to it:
        CREATE database monitoring_app_db;

        psql -h localhost -U postgres -p 5432 -d monitoring_app_db

    Initialize Database Tables:
        python -m monitoring_app.scripts.init_db   

    Create .env file in /monitoring_app package and fill out these variables:
        DB_USER=<username>
        DB_PASSWORD=<password>
        DB_HOST=localhost
        DB_PORT=5432
        DB_NAME=monitoring_app_db
        DISCORD_WEBHOOK_URL=<personal_discord_webhook>    
            
    Insert Initial Endpoints:
        python -m monitoring_app.scripts.insert_endpoints



# Run the App:
    Using default .YAML file:
        python -m monitoring_app.app

    Using custom .YAML file:
        python -m monitoring_app.app <path_to_selected_yaml>

# Usage:
    Retrieve metrics from for monitored endpoints:
        URL: http://localhost:5000/metrics

    Filter endpoint with query parameters (host, since):
        Query by URL httpbin:
            http://localhost:5000/metrics?host=httpbin
        Query by since_seconds=300:
            http://localhost:5000/metrics?since=300
        Query by combined:
            http://localhost:5000/metrics?host=httpbin&since=1200


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)