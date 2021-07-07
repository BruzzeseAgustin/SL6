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
# start sl6
CMD bash ./docker-entrypoint.sh
