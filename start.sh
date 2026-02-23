#!/bin/bash
set -o errexit

cd StockPredictionPortal
gunicorn StockPredictionPortal.wsgi:application --bind 0.0.0.0:$PORT
