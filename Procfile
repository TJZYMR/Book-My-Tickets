web: gunicorn Bookmyshow.wsgi --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate