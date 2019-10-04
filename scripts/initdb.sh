#!/bin/bash

set -e

cd booksapp

python manage.py migrate

