#!/bin/bash

_term() {
  echo "Caught SIGTERM signal!"
  exit 0
}

trap _term SIGTERM
trap _term SIGINT

i=0
while True; do
  echo $i
  i=$((i + 1))
  sleep 5
done
