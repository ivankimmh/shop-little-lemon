#!/bin/sh

postgres_ready() {
    python <<END
import sys
import psycopg2

try:
    print("Connecting to database...")
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${DB_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError as e:
    print(e)
    sys.exit(-1)
sys.exit(0)

END
}

if [ -z "${POSTGRES_DB}" ] || [ -z "${POSTGRES_USER}" ] || [ -z "${POSTGRES_PASSWORD}" ] || [ -z "${DB_HOST}" ] || [ -z "${POSTGRES_PORT}" ]; then
  echo "Missing required environment variables"
  exit 1
fi

until postgres_ready; do
  >&2 echo "Waiting for PostgreSQL..."
  sleep 1
done

echo >&2 "PostgreSQL is availalbe"

# python manage.py makemigrations
# python manage.py migrate

# echo "Database migration completed"

# db_status=$(python manage.py check_db_is_empty)

# echo "Debug: DB Status: $db_status"


# if [ "$db_status" = "empty" ]; then
#   echo "dummy data creation has been started"
#   python manage.py create_dummy_data
#   echo "dummy data has been created"
# else
#     echo "Data already exists, no need to create dummy data"
# fi

exec "$@"