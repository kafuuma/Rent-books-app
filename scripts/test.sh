#!/bin/bash

set -e

cd booksapp

coverage run --source=books/ manage.py test tests
coverage report -m