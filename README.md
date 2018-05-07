[![Build Status](https://travis-ci.org/muthash/Weconnect-v1.svg?branch=feedback)](https://travis-ci.org/muthash/Weconnect-v1)
[![Coverage Status](https://coveralls.io/repos/github/muthash/Weconnect-v1/badge.svg?branch=feedback)](https://coveralls.io/github/muthash/Weconnect-v1?branch=feedback)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7bd206e97cad42958a5290335b80180f)](https://www.codacy.com/app/muthash/Weconnect-v1?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=muthash/Weconnect-v1&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/50bed4e13c381e0462f2/maintainability)](https://codeclimate.com/github/muthash/Weconnect-v1/maintainability)
![DUB](https://img.shields.io/dub/l/vibe-d.svg)

___

## WeConnect

WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with.
___
### Prerequisites

* Python 3.6
____

### Installation

clone the repo:
```
$ git clone https://github.com/muthash/WeConnect.git
```
and cd into the folder:
```
$ /WeConnect
```
create a virtual environment for the project.
```
$ virtualenv --python=python3.6 virtualenv-name
```
and activate virtual environment
```
$ source virtualenv-name/bin/activate
```
Alternatively you can create it using virtualenvwarapper if installed:
```
$ mkvirtualenv --python=python3.6 virtualenv-name
```
> It will be automatically activated, in the future to use it just type:
```
$ workon virtualenv-name
```
Run the command `$ pip install -r requirements.txt` to install necessary libraries.

### Run 

To test our project on your terminal run 

``` export FLASK_APP=run.py```

then

``` flask run ```

on your browser open up [http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)

### Api Endpoints

| Endpoint | Functionality |
| -------- | ------------- |
| POST /api/v1/register | Creates a user account |
| POST /api/v1/login | Logs in a user |
| POST /api/v1/reset-password  | Password reset |
| POST /api/v1/businesses | Register a business |
| GET /api/v1/businesses  | Retrieves all businesses |
| PUT /api/v1/businesses/businessId | Updates a business profile |
| DELETE /api/v1/businesses/businessId | Remove a business |
| GET /api/v1/businesses/'businessId | Get a business |
| POST /api/v1/businesses/businessId/reviews | Add a review for a business |
| GET /api/v1/businesses/businessId/reviews | Get all reviews for a business |

### Testing using postman or curl 

use the API documentation to get sample data of payload [Here](https://dashboard.heroku.com/apps/w3connect)

do not forget to include the headers on your postman 
 - Content-Type: application/json
 - Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiO

make sure to register and login first to get the authorization token.
Copy the token and paste it into the header section, creating an Authorization header. Don't forget to put the word Bearer before the token with a space separating them like this:

```Bearer eyJ0eXATQsImV4cCI6ViIjo1fQ.8ju7doEn6Q8VJ6WXAnBHKlyn8KCkMr....```

### Test /api/v1/register/
    
    curl -H "Accept: application/json"\-H "Content-type: application/json" -X POST \
	-d '{"email": "test@test.com", "password": "test_password"}' \
	http://127.0.0.1:5000/api/v1/register/

### Test /api/v1/login/
    
    curl -H "Accept: application/json" \
	-H "Content-type: application/json" -X POST \
	-d '{"email": "test@test.com", "password": "test_password"}' \
	http://127.0.0.1:5000/api/v1/login/


