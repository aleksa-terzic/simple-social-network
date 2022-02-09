## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Tests](#tests)
* [Usage and Endpoints](#usage-and-endpoints)


## General info
This project is a simple REST API based social network.
	
## Technologies
Project is created with:
* Python 3.10.1
* Django 4.0.2
* Django REST Framework 3.13.1
* Redis 4.1.2
* Celery 5.2.3
	
## Setup
Clone this repo to your desktop and navigate to projects root folder.

Rename `.env.example` to `.env` and add your credentials.

To quickly generate new Django SECRET KEY, just run `keygen.py` from cmd and copy the generated key in .env file.

Run:
```
docker-compose build
docker-compose up
```

### Tests
From projects root folder, enter backend's container shell with:
```
docker exec -it backend_django /bin/bash
```
Then run:
```
pytest
```

## Usage and Endpoints
| Action        | URL           | Method  |
| ------------- |:-------------:| -----:|
| User Signup      | /api/users/signup | POST |
| User Login     | /api/users/login/      |   POST |
| Get User Data | /api/users/<int:pk>/data/      |    GET |
| Get Post List | /api/posts/      |    GET |
| Create Post | /api/posts/      |    POST |
| Get Post | /api/posts/<int:pk>/      |    GET |
| Update Post | /api/posts/<int:pk>/      |    PUT |
| Delete Post | /api/posts/<int:pk>/      |    DELETE |
| Like Post | /api/posts/<int:pk>/like/      |    POST |
| Unlike Post | /api/posts/<int:pk>/unlike/      |    POST |
