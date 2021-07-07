#!/bin/bash

echo 'y' | docker stop container $(docker container ls -aq)

echo 'y' | docker system prune

echo 'y' | docker image prune -a
