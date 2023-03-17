#!/bin/sh

URL="127.0.0.1"
PORT=5000
ID="$1"
TOKEN="$2"

curl -H "Authorization: Bearer $TOKEN" -X DELETE "$URL:$PORT/devices/$ID/config/"
