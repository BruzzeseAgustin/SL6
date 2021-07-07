#!/bin/bash


# docker build -f Dockerfile -t local/mycontainer .
# docker run -ti -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 80:80 local/mycontainer

# create base hadoop cluster docker image
docker pull scientificlinux/sl
docker run -it scientificlinux/sl:6 cat /etc/redhat-release
docker build -f Dockerfile -t grid-sl6:latest .

echo "start grid.magic.iac.es container..."
docker run -p 80:80 \
	-h grid.magic.iac.es \
	--name grid-sl6 \
	--volume /sys/fs/cgroup:/sys/fs/cgroup:ro \
	-d grid-sl6:latest


# get into hadoop master container
docker exec -it grid-sl6 bash

