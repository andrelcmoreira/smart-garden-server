#!/bin/sh

URL="127.0.0.1"
PORT=5000
BODY="{ \"interval\": \"10\", \"group\": \"foogroup\" }"
ID="$1"
TOKEN="$2"

curl -X POST "$URL:$PORT/devices/$ID/config/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$BODY"
