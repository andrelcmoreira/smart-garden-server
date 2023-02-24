#!/bin/sh

URL="127.0.0.1"
PORT=5000
ID="$1"
TOKEN="$2"
BODY='{ "param": "group",  "value": "new-foo-group" }'

curl -X PUT "$URL:$PORT/devices/$ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$BODY"
