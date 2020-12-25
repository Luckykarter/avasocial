# avasocial
REST API Django based simple social network

The purpose of this application is to provide REST API endpoints for serving social network activities.
Description of endpoints can be found in SwaggerUI/Redoc. Links provided in section API Reference

https://github.com/Luckykarter/avabot - The bot that can be used for demonstrating/testing the features of the application

## Third party services used by application
- Hunter - https://hunter.io - e-mail validation
- ClearBit - https://clearbit.com/ - user data enrichment

The handlers for those services can be found in **avasocial/extapps.py**

## Installation
The current built is for Heroku deployment. 
Installation is deployed on: https://avasocial.herokuapp.com/

### Database
For local development - Python builtin database sqllite3 is used.
For Heroku deployment the postgresql database is used.

### Secret keys
The app uses three secret keys that are served from environment variables (or .env file for local development):
- **SECRET_KEY** - Django secret key
- **HUNTER_KEY** - Secret key for Hunter API access
- **CLEARBIT_KEY** - Secret key for ClearBit API access

## API Reference

### SwaggerUI
https://avasocial.herokuapp.com/swagger

<a href="https://avasocial.herokuapp.com/swagger" target="_blank">
<img src="http://validator.swagger.io/validator?url=https://avasocial.herokuapp.com/swagger.yaml" >
</a>

### Redoc (OpenAPI specification)
https://avasocial.herokuapp.com/redoc

### Postman collection (for tests)
Postman collection including basic tests for endpoints can be found under the following link:

https://www.getpostman.com/collections/7472d2fd7045f06407f0


## Authorization
User sign up does not require any authorization.

All other endpoints are required registered user to be signed-in using JWT token.
Please refer to the description of /user/login/ endpoint. For additional information - visit https://jwt.io/

## Used libraries
Please refer to requirements.txt for the full list of dependencies. 

Some information about the choosen libraries:
- django-heroku - used for Heroku deployment
- djangorestframework-simplejwt - for convenient access to JWT functionality
- drf-yasg - "yet another swagger generator". For generating Swagger/Redoc documentation
- gunicorn - for web-deployment
- pyhunter - wrapper for convenient access to Hunter web-services
- python-dotenv - for local storage of secret keys in .env file
- clearbit - wrapper for convenient access to ClearBit web-services


