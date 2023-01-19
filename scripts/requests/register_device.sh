#!/bin/sh

URL="127.0.0.1"
PORT=5000
BODY='{ "user": "andre", "token": "foo", "device-id": "id", "serial-number": "number", "description": "foo desc", "group": "some group" }'

curl -X POST $URL:$PORT/register/ \
  -H 'Content-Type: application/json' \
  -d "$BODY"
