# Django Online Store

## Setup

The first thing to do is to clone the repository:

```sh
git clone https://github.com/AymanRefat/django-shop
cd django-shop
```

Create a virtual environment to install dependencies in and activate it:

```sh
  py -m venv env 
  env/Scripts/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:

```sh
(env)$ cd project
(env)$ python manage.py runserver
```

## Walkthrough

After starting the server you can ues the app only go to `http://127.0.0.1:8000`,
and you will get the Root Page .


## Tests

To run the tests, `cd` into the directory where `manage.py` is:

```sh
(env)$ python manage.py test
```
