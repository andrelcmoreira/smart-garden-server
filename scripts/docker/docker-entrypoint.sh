#!/bin/sh

echo ' * Waiting db...'
while ! python wait_db_container.py 2> /dev/null ; do
  sleep 2
done

echo ' * Running app...'
python app/run.py
