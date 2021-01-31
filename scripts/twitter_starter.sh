#!/bin/bash

set -e

# python manage.py collectstatic --noinput
echo "Starting $NAME as `whoami`"
NAME="twitter"                              #Name of the application (*)
DJANGODIR=/home/appadmin/acsz/           # Django project directory (*)
SOCKFILE=/tmp/twitter.sock        # we will communicate using this unix socket (*)
USER=appadmin                                        # the user to run as (*)
GROUP=appadmin                                     # the group to run as (*)
NUM_WORKERS=2                                   # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=django_twitter.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=django_twitter.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
#source  /home/kathir/anaconda3/etc/profile.d/conda.sh

echo $DJANGO_WSGI_MODULE

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
python manage.py collectstatic <<<yes


exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=0.0.0.0:8000 #unix:/tmp/data-extractor.sock
