#!/bin/sh

URL="127.0.0.1"
PORT=5000
ID="$1"
TOKEN="$2"
BODY='{ "param": "dev_group",  "value": "new-foo-group" }'

curl -X PUT "$URL:$PORT/devices/$ID/config/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$BODY"
