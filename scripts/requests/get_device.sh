#!/bin/sh

URL="127.0.0.1"
PORT=5000
ID="$1"

curl "$URL:$PORT/devices/$ID"
