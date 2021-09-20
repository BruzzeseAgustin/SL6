#!/bin/bash


# docker build -f Dockerfile -t local/mycontainer .
# docker run -ti -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 80:80 local/mycontainer

# create base hadoop cluster docker image
docker pull scientificlinux/sl
docker run -it scientificlinux/sl:6 cat /etc/redhat-release
docker build -f Dockerfile -t grid.magic.iac-test.pic.es:latest .

echo "start grid.magic.iac.es container..."
docker run -p 80:80 \
	--net=host \
	-p 2814:2814 \
	-p 2813:2813 \
	-p 2811:2811 \
	-p 20000-22000:20000-22000 \
	-p 50000-51000:50000-51000 \
	-h grid.magic.iac-test.pic.es \
	--name grid.magic.iac-test.pic.es \
	--volume $(pwd)/data/:/data \
	--volume /sys/fs/cgroup:/sys/fs/cgroup:ro \
        --volume $(pwd)/psql-data:/psql-data \
        --volume $(pwd)/mysql-data:/mysql-data \
	--volume /etc/grid-security/:/etc/grid-security/ \
        --volume /etc/vomses:/etc/vomses \
        --volume $(pwd)/cert/grid_magic_iac-test_pic_es.pem:/etc/grid-security/hostcert.pem \
        --volume $(pwd)/cert/hostkey.grid.magic.iac-test.pic.es.pem:/etc/grid-security/hostkey.pem \
        --volume $(pwd)/cert/grid_magic_iac-test_pic_es.pem:/var/lib/globus-connect-server/grid-security/hostcert.pem \
        --volume $(pwd)/cert/hostkey.grid.magic.iac-test.pic.es.pem:/var/lib/globus-connect-server/grid-security/hostkey.pem \
	--volume $(pwd)/grid-mapfile:/etc/grid-security/grid-mapfile \
	--volume $(pwd)/gridftp.conf:/etc/gridftpd/gridftpd_backend/ \
	-d grid.magic.iac-test.pic.es:latest

# Please provide the full path to the Globus GridFTP server binary [/usr/sbin/globus-gridftp-server]: 

# Please provide the full path to the GSI configuration base dir [/etc/grid-security]: 

# Please provide the full path to the grid-mapfile to use for this service [/etc/grid-security/grid-mapfile]: 

# Please provide the full path to the trusted CA certificates dir to use for this service [/etc/grid-security/certificates]: 

# Please provide the full path to the host certificate used for the front end [/etc/grid-security/hostcert_grid.magic.iac.es_frontend.pem]:

# Please provide the full path to the host key used for the back end(s) [/etc/grid-security/hostkey_grid.magic.iac.es_backend.pem]: 

# Please use the following string (without double quotes!) on the remote systems when asked for additional GridFTP back ends: "grid.magic.iac.es:2813,grid.magic.iac.es:2814"
 
# get into hadoop master container
docker exec -it grid.magic.iac-test.pic.es bash

