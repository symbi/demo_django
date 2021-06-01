#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
#python manage.py flush --no-input
#python manage.py migrate
sleep 5
#python3 setup.py
python3 manage.py makemigrations
python3 manage.py migrate
#python3 manage.py collectstatic --noinput
chmod 777 mm.sh
chmod 777 mg.sh
# uwsgi --socket :8001 --module mysite.wsgi

exec "$@"
