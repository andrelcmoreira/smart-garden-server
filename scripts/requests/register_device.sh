#!/bin/sh

URL="127.0.0.1"
PORT=5000
BODY='{ "user": "foo-user", "token": "foo-token", "device-id": "foo-id", "serial-number": "foo-number", "description": "foo-desc", "group": "foo-group" }'

curl -X POST $URL:$PORT/register/ \
  -H 'Content-Type: application/json' \
  -d "$BODY"
