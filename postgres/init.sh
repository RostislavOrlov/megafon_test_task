set -e

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
	CREATE DATABASE megafon OWNER postgres;
EOSQL

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "megafon" -f /app/sql/init.sql
