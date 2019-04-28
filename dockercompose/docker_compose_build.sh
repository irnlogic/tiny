#!/bin/bash
rm -rf ./django/src
cp  -R ../src  ./django
docker-compose build
rm -R ./django/src




