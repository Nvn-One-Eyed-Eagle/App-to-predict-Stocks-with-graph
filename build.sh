#!/bin/bash
set -o errexit

pip install -r requirements.txt
cd StockPredictionPortal
python manage.py collectstatic --noinput
python manage.py migrate

echo "==> Build complete. To start: bash start.sh"
