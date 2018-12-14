# 分布式服务部署架构
分布式服务部署架构：实现分布服务系统多分支热部署

### 依赖软件（宿主主机）
- jenkins
- docker

### 软件依赖（docker容器内）
- sshd
- nginx
- zookeeper
- tomcat
- jdk8+


# 特性
### 主要特性
- 支持动态添加删除jenkins的视图、任务
- 支持多分支急速构建
- 支持热部署
- 支持apm

### 极端场景(待优化)
- 服务在处理请求的过程中被强制下线


# 核心架构
![baidu](https://graph.baidu.com/resource/18b656ffd5e79d867884001543991825.jpg)

### 新分支部署流程
1. 通过jenkins任务执行视图、任务的构建、容器创建
2. 拉取分支代码、复制系统环境资源、构建jar、war
3. 容器内完成jdk、zk、nginx、服务部署
4. 启动所有服务

### 服务热部署
1. jenkins构建服务
2. 容器内创建服务或备份服务
3. 服务或备份服务启动完成后，kill已存在服务或备份服务

### 用户调用流程
1. 用户请求宿主主机端口
2. 主机代理至docker中nginx(也可是其他端口代理工具)
3. nginx将请求分布至web应用

# 文档说明
### 配置文档
```
[global]
jenkins任务路径#
mvn_path=/xxx/mvn
ln_log_dst_path=日志软连接路径(可优化未elk采集日志)

[jenkins]
#jenkins全局配置
config_xml_path=/xxx/config.xml
#jenkins任务路径
job_dst_path=/xxx/jobs

[template]
#项目源码路径
src_path=/xxx
#编译后的jar、war输出路径
dst_path=/xxx
#用于覆盖项目源码里资源的本地资源路径
env_path=/xxx
#生产者服务列表
producer_list=user,loan,payment,invest,secondary
#消费者服务列表
customer_list=management,financial,api,bi
#消费者服务端口列表，与customer_list服务位置一一对应
customer_port_list=8080,8081,8082,8083
#项目分支名称，默认值master
branch_name=master
#宿主主机端口，映射到容器中的nginx端口
proxy_tomcat_port=8984
#宿主主机端口，映射到容器中sshd端口
proxy_ssh_port=22
#宿主主机端口，映射到容器中zk端口
proxy_zk_port=8021
#动态切换的服务后缀名，默认值为_backup
backup_suffix=_backup
#生产者服务名称前缀，默认finance-
producer_prefix=
#生产者服务名称后缀，默认-service
producer_suffix=
#消费者服务名称前缀，默认hk-
customer_prefix=
#消费者服务名称后缀，默认值-services
customer_suffix=
#版本后缀，默认值-1.0-SNAPSHOT
version=
```

### 脚本使用
- 待完善
