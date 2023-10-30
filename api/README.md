# AIR BNB Clone API
## Description
This is the API for the Air BNB Clone project. It is written in Python using the Flask framework. It is connected to a MySQL database using SQLAlchemy. It is deployed on an Ubuntu server using Gunicorn and Nginx.

## API Routes
### /status
Returns the status of the API
```
{
    "status": "OK"
}
```
### /stats
Returns the number of each object in the database
```
{
    "amenities": 3,
    "cities": 3,
    "places": 3,
    "reviews": 3,
    "states": 3,
    "users": 3
}
```