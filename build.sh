#!/bin/bash
set -e

# Apply migrations for all apps, including 'orders'
python manage.py makemigrations orders --noinput
python manage.py migrate

# Create admin user
python manage.py create_admin

# Collect static files
python manage.py collectstatic --noinput