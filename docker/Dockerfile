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
COPY Shanghai /etc/localtime
COPY get-pip.py /etc/
COPY profile /etc/

#enable sshd
RUN rm -rf /etc/service/sshd/down
#RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
RUN /bin/echo 'root:Docker@123'|chpasswd

#install nginx
RUN apt-get update && apt-get install -y nginx
RUN apt-get install -y net-tools

#install python3, Ubuntu 16.04 had installed python3.5.2
#add-apt-repository ppa:jonathonf/python-3.6 && apt-get install python3.6
RUN python3 /etc/get-pip.py && pip install coloredlogs

# Clean up APT when done.
RUN echo 'Asia/Shanghai' >/etc/timezone && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Define commonly used JAVA_HOME variable
#ENV JAVA_HOME /opt/jdk

#暴露端口
EXPOSE 5000-5010
EXPOSE 5100-5110
EXPOSE 7000-7010
EXPOSE 7100-7110

# Define default command.
CMD ["/sbin/my_init"]






