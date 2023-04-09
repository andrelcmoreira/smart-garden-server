#!/bin/sh

URL="127.0.0.1"
PORT=5000
ID="$1"
SERIAL="$2"
BODY="{ \"id\": \"$ID\", \"serial-number\": \"$SERIAL\" }"

curl -X POST "$URL:$PORT/devices/login/" \
  -H "Content-Type: application/json" \
  -d "$BODY"
