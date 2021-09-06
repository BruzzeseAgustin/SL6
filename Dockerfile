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

RUN yum install -y sudo \
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
	tree

# start sl6
CMD bash ./docker-entrypoint.sh
