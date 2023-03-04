#!/bin/sh

URL="127.0.0.1"
PORT=5000
DEVICES="foo bar baz qux"
TOKEN="$1"

for dev in $DEVICES; do
  BODY="{ \"model\": \"$dev-model\", \"serial-number\": \"$dev-serial\", \"description\": \"\" }"

  curl -X POST "$URL:$PORT/devices/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "$BODY"
done
