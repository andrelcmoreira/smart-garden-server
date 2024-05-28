#!/bin/sh

URL="127.0.0.1"
PORT=5000
BODY='{ "user": "admin", "password": "_p@$$w0rd_" }'

curl -X POST "$URL:$PORT/login/" \
  -H "Content-Type: application/json" \
  -d "$BODY"
