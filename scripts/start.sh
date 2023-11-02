#! /bin/sh

echo "서버 시작"

python manage.py collectstatic --no-input

# upload collected static files

python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '1234')" | python manage.py shell

gunicorn LittleLemon.wsgi:application --config LittleLemon/gunicorn_config.py