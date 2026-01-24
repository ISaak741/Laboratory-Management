#!/bin/bash

set -e

cat .env.example > .env

echo "Starting Database Setup..."

flask db init

flask db migrate -m "Initial Docker migration"

flask db upgrade

echo "Database is ready. Starting Flask..."

exec python app.py