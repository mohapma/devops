# https://github.com/AdoptOpenJDK/openjdk-docker/blob/master/11/jdk/alpine/Dockerfile.hotspot.releases.full
FROM adoptopenjdk/openjdk11:alpine AS confd

RUN apk add --no-cache --update curl
        
ARG CONFD_VERSION=0.16.0

RUN curl -SL https://github.com/kelseyhightower/confd/releases/download/v${CONFD_VERSION}/confd-${CONFD_VERSION}-linux-amd64 -o /usr/local/bin/confd

# build springboot service
FROM adoptopenjdk/openjdk11:alpine

MAINTAINER DL-CP-DEVOPS <DL-CP-DEVOPS@tecnotree.com>

ARG RELEASE="5.0.0-SNAPSHOT"
ARG SPRINGBOOT_APP_JAR="customer-management.jar"

LABEL vendor=Tecnotree \
      service=dclm-customer-management \
      release_tags="[\"${RELEASE}\"]"

# set configurable USERNAME group
ARG UID=860
ARG GID=860
ARG USERNAME=tomcat
ARG GROUPNAME=tomcat
ARG USER_HOME=/home/${USERNAME}
ARG TOMCAT_BASE=/usr/local/tomcat

# update alpine and install required tools, su-exec (gosu-compatible) for step-down from root
RUN apk add --no-cache --update \
        su-exec \
        bash

# add confguration management confd
COPY --from=confd /usr/local/bin/confd /usr/local/bin/confd
RUN chmod a+x /usr/local/bin/confd

# copy confd templates to inject configuration
COPY docker/config/confd /etc/confd

# copy application.properties as a template and let confd re-generate application.properties
RUN mkdir -p /etc/confd/templates
COPY dclm/customer-management/target/config/application.properties /etc/confd/templates/application.properties.tmpl

WORKDIR ${TOMCAT_BASE}

# create springboot tomcat directories
RUN mkdir -p ${TOMCAT_BASE}/config ${TOMCAT_BASE}/logs

# copy springboot application
COPY dclm/customer-management/target/${SPRINGBOOT_APP_JAR} ${TOMCAT_BASE}/

# create username (to go "non-root") and grant directory permissions
RUN addgroup --system --gid ${GID} ${GROUPNAME} && \
    adduser --system --home ${USER_HOME} --shell /bin/bash --uid ${UID} --ingroup ${GROUPNAME} --disabled-password ${USERNAME} && \
    chown -R ${USERNAME}:${GROUPNAME} ${USER_HOME} && \
    chown -R ${USERNAME}:${GROUPNAME} ${TOMCAT_BASE}
        
# add entrypoint script to start springboot
ADD docker/scripts/docker-entrypoint.sh /
RUN chmod a+x /docker-entrypoint.sh

# persist app logs not send to stdout log management 
VOLUME ${TOMCAT_BASE}/logs

# set default environment properties for the springboot
ENV SERVER_PORT=8080 \
    LOG_LEVEL=INFO \
    JAVA_OPTS='-Xms4g -Xmx4g' \
    TOMCAT_BASE=${TOMCAT_BASE} \
    TOMCAT_MAX_CONNECTIONS=100 \
    TOMCAT_MAX_THREADS=10 \
    TOMCAT_MIN_SPARE_THREADS=5 \
    SPRINGBOOT_APP_JAR=${SPRINGBOOT_APP_JAR} \
    USERNAME=${USERNAME} \
    GROUPNAME=${GROUPNAME}

# expose springboot port HTTP
EXPOSE 8080
    
ENTRYPOINT ["/docker-entrypoint.sh"]
