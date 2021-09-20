#!/bin/bash

DOCKER_CONTAINER_LIST=$(docker ps -a -q)
echo 'y' | docker stop $DOCKER_CONTAINER_LIST; 
docker rm $DOCKER_CONTAINER_LIST; 

