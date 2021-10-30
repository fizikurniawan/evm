#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collect static files"

# create media and static dir
mkdir -p static upload

# uncomment STATIC_ROOT
sed -i -e 's/\# STATIC_ROOT/STATIC_ROOT/g' project/settings.py

# collecting statics
python manage.py collectstatic --noinput

# comment again
sed -i -e 's/STATIC_ROOT/\# STATIC_ROOT/g' project/settings.py

# uncomment static dir
sed -i -e 's/\# os.path.join(BASE_DIR, "static"),/os.path.join(BASE_DIR, "static"),/g' project/settings.py


# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
