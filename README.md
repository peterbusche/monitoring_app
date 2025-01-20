Symbol key:
    ->currently using
    *potential to use
    **secondary potential



Technologies Used
1)Entry Point Language: 
    ->Python
    *Ruby
    **GO

2)Database
    ->PostgreSQL

    ORM to avoid Sql queries? 
        ->SQL Alchemy    

2)Scheduler: 
    ->APScheduler
    *asyncio

3)Notification Service:
    ->Discord (Discord Webhooks)
    *Slack (Slack Webhooks)

4)Monitoring Endpoint:
    ->Flask
    *Django


[If I have time]
5)Frontend
    Framework:
        -> TBD
    Graphs:
        ->TBD

6)Hosting
    Cloud:
        ->TBD
    Containers:
        ->TBD
    CI/CD:
        ->TBD



Potential request targets:
    example.com
    httpbin.org
    jsonplaceholder.typicode.com


Potential project Structure:
/my_monitoring_app
  -> app.py           # Entry point with Flask + APScheduler
  -> db.py            # Database setup (SQLAlchemy engine, session)
  -> models.py        # SQLAlchemy models/tables
  -> scheduler.py     # APScheduler job definitions
  -> requirements.txt



THINGS TO INCLUDE
    What this does
    how to configure it
    how to test it
