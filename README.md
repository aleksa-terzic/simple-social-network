## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Tests](#tests)
* [Usage and Endpoints](#usage-and-endpoints)


## General info
This project is a simple REST API based social network.

JWT Tokens are used for user authentication.

Users can sign up, login, view other users posts, create posts and like/unlike posts.

For Email, Geodata and Holiday purposes, recommended 3rd party API is used (AbstractAPI).

On user signup, email is validated if it is deliverable. If the check came back positive, user is added to the database.

While that executes, in the background, Celery worker picks up a task and enriches user's profile with data like country and city from where the signup originated from.

Also, it checks if the signup date coincides with holiday in user's country and adds it to his profile, not affecting users ability to browse the website, since Celery executes it in the background through its messaging broker, Redis.
	
## Technologies
Project is created with:
* Python 3.10.1
* Django 4.0.2
* Django REST Framework 3.13.1
* Redis 4.1.2
* Celery 5.2.3
	
## Setup

1. Clone this repo to your desktop and navigate to projects root folder.
2. Rename `.env.example` to `.env` and update the environment variables.
3. Build the images and run the containers:
```
docker-compose up -d --build
```
Now everything is built and running, you can confirm it by visiting http://localhost:8000/ in your browser.
--Currently no schema at front page, tbd

Note: To quickly generate new SECRET KEY, just run `keygen.py` from cmd and copy the generated key in .env file.

### Tests
From projects root folder, enter backend's container shell with:
```
docker exec -it backend_django /bin/bash
```
Then run:
```
pytest
```
Tests should now execute and you will be able to see the results and coverage of tests.

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
