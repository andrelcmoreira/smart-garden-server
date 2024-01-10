#!/bin/sh

echo ' * Waiting db...'
while ! python scripts/db/wait_db.py 2> /dev/null ; do
  sleep 2
done

echo ' * Running app...'
python app/run.py
