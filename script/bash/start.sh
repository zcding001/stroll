#!/bin/sh

#------------------------------------------------------------------------
#author		    :	zc.ding
#date		    :	2018-12-05
#filename	    :	start
#description	:	服务启动脚本 
#
#-----------------------------------------------------------------------

export JRE_HOME=/share/soft/jdk/jre

readonly SEC_NAME=$1
readonly SERVICE_NAME=$2
readonly DEBUG_PORT=$3
readonly ACTION=$4
readonly SERVICE_PATH="/share/projects/"${SEC_NAME}"/finance-"${SERVICE_NAME}"-service"
readonly JAR_NAME=${SERVICE_NAME}"-1.0-SNAPSHOT.jar"
readonly PID="service.pid"
readonly SERVICE_LOG="service.log"

cd ${SERVICE_PATH}
java_agent_path=${SERVICE_PATH}/agent/skywalking-agent.jar
java_agent=''
[[ -f ${java_agent_path} ]] && java_agent='-javaagent:'${java_agent_path}

echo "" > ${SERVICE_LOG}
case "${ACTION}" in
    start)
	    nohup ${JRE_HOME}/bin/java ${java_agent} -jar -Xms256m -Xmx256m -Xdebug -Dsun.zip.disableMemoryMapping=true \
	    -Xrunjdwp:transport=dt_socket,address=${DEBUG_PORT},server=y, suspend=n ${JAR_NAME} >>${SERVICE_LOG} 2>&1 &
        echo $! > ${PID}
        echo "=== start ${SERVICE_NAME}"
        ;;

    stop)
        kill `cat ${PID}`
        rm -rf ${PID}
        echo "=== stop ${SERVICE_NAME}"
        sleep 5
        pid=`ps -ef | grep -w "${SERVICE_NAME}" | grep -v "grep" | awk '{print $2}'`
        if [[ "${pid}" == "" ]]; then
            echo "=== ${SERVICE_NAME} process not exists or stop success"
        else
            echo "=== ${SERVICE_NAME} process pid is:${pid}"
            echo "=== begin kill $SERVICE_NAME process, pid is:${pid}"
            kill -9 ${pid}
        fi
        ;;

    restart) 
        $0 stop
        sleep 2
        $0 start
        echo "=== restart ${SERVICE_NAME}"
        ;;

    *)
        ## restart
        $0 stop
        sleep 5
        $0 start
       ;;
esac
exit 0
