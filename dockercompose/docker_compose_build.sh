#!/bin/bash
rm -rf ./django/src
cp  -R ../src  ./django
#docker-compose build
docker-compose build --no-cache
rm -R ./django/src




