#!/bin/sh

URL="127.0.0.1"
PORT=5000
BODY="{ \"model\": \"foo-model\", \"serial-number\": \"foo-serial\", \"description\": \"\" }"
TOKEN="$1"

curl -X POST "$URL:$PORT/devices/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$BODY"
