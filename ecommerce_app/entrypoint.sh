#!/usr/bin/env sh
set -e

DB_HOST=${DB_HOST:-127.0.0.1}
DB_PORT=${DB_PORT:-3306}
DB_NAME=${DB_NAME:-${MYSQL_DATABASE:-ecommerce_db}}
DB_USER=${DB_USER:-${MYSQL_USER:-app}}
DB_PASSWORD=${DB_PASSWORD:-${MYSQL_PASSWORD:-app}}
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD:-root}
MYSQL_DATABASE=${MYSQL_DATABASE:-$DB_NAME}
MYSQL_USER=${MYSQL_USER:-$DB_USER}
MYSQL_PASSWORD=${MYSQL_PASSWORD:-$DB_PASSWORD}

export DB_HOST DB_PORT DB_NAME DB_USER DB_PASSWORD
export MYSQL_ROOT_PASSWORD MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD

start_local_db() {
  mkdir -p /var/run/mysqld /var/lib/mysql
  chown -R mysql:mysql /var/run/mysqld /var/lib/mysql

  if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "Initializing local database..."
    mariadb-install-db --user=mysql --datadir=/var/lib/mysql >/dev/null

    mysqld --user=mysql --datadir=/var/lib/mysql --skip-networking --socket=/var/run/mysqld/mysqld.sock &
    until mysqladmin ping --socket=/var/run/mysqld/mysqld.sock --silent; do
      sleep 1
    done

  else
    mysqld --user=mysql --datadir=/var/lib/mysql --skip-networking --socket=/var/run/mysqld/mysqld.sock &
    until mysqladmin ping --socket=/var/run/mysqld/mysqld.sock --silent; do
      sleep 1
    done
  fi

  if mysql --socket=/var/run/mysqld/mysqld.sock -uroot -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT 1" >/dev/null 2>&1; then
    mysql_auth="-uroot -p${MYSQL_ROOT_PASSWORD}"
  else
    mysql_auth="-uroot"
  fi

  mysql --socket=/var/run/mysqld/mysqld.sock ${mysql_auth} <<-SQL
      ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';
      CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE}\`;
      CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
      CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
      GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* TO '${MYSQL_USER}'@'%';
      GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* TO '${MYSQL_USER}'@'localhost';
      FLUSH PRIVILEGES;
SQL

  mysqladmin --socket=/var/run/mysqld/mysqld.sock -uroot -p"${MYSQL_ROOT_PASSWORD}" shutdown

  mysqld --user=mysql --datadir=/var/lib/mysql --bind-address=0.0.0.0 &
}

if [ "$DB_HOST" = "localhost" ] || [ "$DB_HOST" = "127.0.0.1" ]; then
  start_local_db
fi

echo "Waiting for database..."
python - <<'PY'
import os
import sys
import time

import MySQLdb

host = os.getenv("DB_HOST", "127.0.0.1")
port = int(os.getenv("DB_PORT", "3306"))
user = os.getenv("DB_USER", "app")
password = os.getenv("DB_PASSWORD", "app")
name = os.getenv("DB_NAME", "ecommerce_db")

timeout = 60
start = time.time()
while True:
    try:
        conn = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=name,
        )
        conn.close()
        break
    except Exception as exc:
        if time.time() - start > timeout:
            print(f"Database not ready: {exc}", file=sys.stderr)
            sys.exit(1)
        time.sleep(2)
PY

python manage.py migrate --noinput

exec "$@"
