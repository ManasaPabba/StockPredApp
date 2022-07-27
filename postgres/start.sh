#!/bin/sh

# You could probably do this fancier and have an array of extensions
# to create, but this is mostly an illustration of what can be done

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<EOF
CREATE EXTENSION plpython3u;
CREATE EXTENSION tspdb;
CREATE USER demo WITH  PASSWORD '00' SUPERUSER
EOF