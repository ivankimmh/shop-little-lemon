#! /bin/sh

echo start server

python manage.py collectstatic --no-input

# upload collected static files

python manage.py makemigrations
python manage.py migrate
gunicorn LittleLemon.wsgi:application --config LittleLemon/gunicorn_config.py