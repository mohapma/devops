#!/bin/bash

set -eu

: ${TOMCAT_BASE:?must be set!}

# update applications.properties 
if [ -s "/etc/confd/templates/application.properties.tmpl" ] ; then
  /usr/local/bin/confd -confdir="/etc/confd" -onetime -backend env
fi

# exec spring-boot service as unpriveleged non-root USER. 

# stream access_log to container console since unprivileged child process cannot write to container /dev/stdout 
touch ${TOMCAT_BASE}/logs/access_log.log && tail -F ${TOMCAT_BASE}/logs/access_log.log &
chown -R ${USERNAME}:${GROUPNAME} ${TOMCAT_BASE}

cd ${TOMCAT_BASE}
exec su-exec ${USERNAME}:${GROUPNAME} java $JAVA_OPTS -jar ${TOMCAT_BASE}/${SPRINGBOOT_APP_JAR} $@
