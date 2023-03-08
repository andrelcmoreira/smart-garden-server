#!/bin/sh

URL="127.0.0.1"
PORT=5000
TOKEN="$1"

curl -H "Authorization: Bearer $TOKEN" "$URL:$PORT/devices/"
