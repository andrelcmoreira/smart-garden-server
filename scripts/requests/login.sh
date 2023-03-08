#!/bin/sh

URL="127.0.0.1"
PORT=5000
BODY='{ "user": "admin", "password": "admin" }'

curl -X POST "$URL:$PORT/login/" \
  -H "Content-Type: application/json" \
  -d "$BODY"
