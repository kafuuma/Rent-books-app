#!/bin/bash


set -e
set -o pipefail # if any code doesn't return 0, exit the script


scripts/initdb.sh

cd booksapp

function start_server() {
  if [[ $ENVIRONMENT == "production" ]]; then
    echo Starting Gunicorn server..
    exec gunicorn booksapp.wsgi:application \
      --bind 0.0.0.0:8080 \
      --workers 3
  else
    echo Starting Django development server..
    python manage.py runserver 0.0.0.0:8080

  fi
}

start_server

exit 0