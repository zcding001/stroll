#
#多分支无等待测试环境部署
#
#author		:	zc.ding
#date		:	2018-08-16
#filename	:	Dockerfile
#
#
FROM phusion/baseimage:0.10.1


COPY sshd_config /etc/ssh/sshd_config

#enable sshd
RUN rm -rf /etc/service/sshd/down 
#RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
RUN /bin/echo 'root:Docker@123'|chpasswd


COPY Shanghai /etc/localtime

#install nginx
RUN apt-get update && apt-get install -y nginx
# Clean up APT when done.
RUN echo 'Asia/Shanghai' >/etc/timezone && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Define commonly used JAVA_HOME variable
#ENV JAVA_HOME /share/soft/jdk

#暴露端口
EXPOSE 5100-5150
# Define default command.
CMD ["/sbin/my_init"]






