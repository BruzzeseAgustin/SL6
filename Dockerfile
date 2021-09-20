# Example SL6 systemd Dockerfile
FROM sl:6
ENV container docker
### This example enables httpd via systemd within the container

# RUN yum -y install httpd \ 
# 	&& yum clean all \
# 	&& systemctl enable httpd.service
EXPOSE 80
### End of example commands for httpd via systemd
VOLUME [ "/sys/fs/cgroup" ]
# CMD ["/usr/sbin/init"]

# CMD ["/bin/bash"]
ADD config/ /
ADD yum.repos/ /etc/yum.repos.d/
ADD psql-connector.py / 
ADD mysql-connector.py /
ADD renew_proxy.sh /
ADD creation_smbk_link.py / 
ADD run_script.sh /

RUN yum -y install epel-release \
	&& yum upgrade -y \
	&& yum -y install curl \
	sudo \
	wget \
	mlocate \
	postgresql-server \
	postgresql-contrib \
	postgresql-jdbc* \
	kernel \ 
	kernel-tools \ 
	kernel-tools-libs \
	python-devel \
	postgresql-devel \
	python-dev \
	python-pybabel \
	python-psycopg2 \
	mysql-server \
	MySQL-python \
	nano \
        && yum clean all \
	&& rm -rf /var/cache/yum/* \
	&& yum upgrade -y \
	&& yum -y install --enablerepo="epel" mysql-utilities \
	mysql-connector-python \
	supervisor \
	globus-gridftp-server \ 
	globus-connect-server \
	voms-clients3 \ 
	voms-clients-java 

RUN yum install -y https://downloads.globus.org/toolkit/gt6/stable/installers/repo/rpm/globus-toolkit-repo-latest.noarch.rpm \
	&& yum install -y globus-connect-server \
	libudt* \ 
	apr* \
	cronie* \ 
	crontab \
	python34 \
        && yum clean all \
        && rm -rf /var/cache/yum/*
 
RUN yum install -y libudt* apr* cronie* crontab \
	python34 \
        && yum clean all \
        && rm -rf /var/cache/yum/*

RUN groupadd transfer \
	&& useradd -r -g transfer -s /bin/bash transfer 

# RUN yum install -y globus-gridftp-server globus-connect-server voms-clients3 voms-clients-java 

RUN mkdir -p /etc/grid-security/ \
	&& mkdir -p /data/Other/rucio_tmp/ \
	&& chmod 777 /data/Other/rucio_tmp/ \
	&& chmod 777 -R /var/log

# Adding server config file to container
ADD globus-connect-server.conf /etc/globus-connect-server.conf

# RUN wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
# RUN yum install -y epel-release-latest-7.noarch.rpm
# RUN yum install -y https://downloads.globus.org/toolkit/gt6/stable/installers/repo/rpm/globus-toolkit-repo-latest.noarch.rpm
# RUN yum install -y globus-connect-server
RUN chown transfer: -R /data

# echo "" | sudo service mysqld start
# su mysql
# echo "CREATE DATABASE magic;" | mysql -u root
# mysql -u root -p magic < /mysql-data/TRANSFER.sql 
# mysql -u root -p magic < /mysql-data/STORAGE.sql 

# /etc/init.d/globus-gridftp-server restart
# start sl6
CMD bash ./docker-entrypoint.sh

EXPOSE 2814
# Please provide the TCP port the first back end should listen to (additional backends will use the subsequent TCP ports, so make sure you have enough unused ports in this range) [2813]: 
EXPOSE 2813
# Please provide the TCP port the front end should listen to [2811]: 
EXPOSE 2811
# inbound connections (GLOBUS_TCP_PORT_RANGE) [20000,25000]
# outbound connections (GLOBUS_TCP_SOURCE_RANGE) [20000,25000]:
EXPOSE 20000-25000

EXPOSE 50000-51000 

#Exposing ports Globus's MyProxy uses
EXPOSE 7512

#Exposing ports Globus's OAuth uses
EXPOSE 443
