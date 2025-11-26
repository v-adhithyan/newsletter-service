# newsletter-service
Developed using Python (3.13), Django & SQLite (db)

## How to run?
- Clone this repo and open in terminal.
- Create a virtual env `python -m venv venv` (only first time)
- Activate virtualenv `source venv/bin/activate`
- Install requirements `pip install -r requirements.txt` (only first time)
- Run server `python manage.py runserver`

## Accessing the UI
- Run this command to create a superuser as it required to access Django admin which is an inbuilt cms utility provided by Django to manage database models without writing code or with minimal code.
- The project heavily uses django admin to add Topic, Content, Subscribers.
- `python manage.py createsuperuser` - follow the onscreen instructions to create username and password
- Server starts running in port 8000. Hit http://localhost:8000/admin and use the username and password you created previously and you will be able to see an UI like this


![demo.png](screenshots/demo.png)


## Assumptions

- My goal was to keep everything simple. This is because since this project also needs to be deployed, having many moving parts like database, cache or message queues will be too complex for now.
- SQLite is used as the primary source of truth because it is light weight and can be created inside the server where the app is running. If we opt for postgres or mysql, we need to use cloud providers when the app gets deployed.

## How the app works?

## Limitations