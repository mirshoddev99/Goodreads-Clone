## GoodReads Clone
This is a clone of the popular book review and recommendation website, Goodreads. It was built using the Django web framework and utilizes Celery and RabbitMQ for sending emails. This project also includes a RESTful API and comprehensive test cases for all its features.

# Features
- User authentication and authorization

- CRUD operations for books and reviews

- Recommendation system based on book ratings

- Ability to send email notifications using Celery and RabbitMQ

- RESTful API for all features

- Comprehensive test cases

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

# Prerequisites
You need to have Python and pip installed on your machine. You can download the latest version of Python here.

# Installing
1. Clone the repository:
bash

git clone https://github.com/mirshoddev99/goodreads-clone.git

2. Change into the project directory
bash
cd goodreads-clone

3. Create a virtual environment and activate it
bash
python -m venv env
source env/bin/activate

4. Install the required packages
pip install -r requirements.txt

5. Run the migrations
python manage.py migrate

6. Start the Celery worker
celery -A goodreads_clone worker -l info

7. Start the Django development server
python manage.py runserver

The application will be running on http://localhost:8000. The API endpoint will be at http://localhost:8000/api/.

# Running the tests
To run the test cases, use the following command:
python manage.py test

# Built With
Django - The web framework used

Django Rest Framework - RESTful API framework

Celery - Task queue for sending emails

RabbitMQ - Message broker for Celery

# Contributing
If you'd like to contribute to this project, please fork the repository and make your changes. Once you've made your changes, you can submit a pull request for review.
