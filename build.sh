#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements-prod.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Load initial sample data and photos automatically
echo "Loading initial data..."
python load_initial_data.py
