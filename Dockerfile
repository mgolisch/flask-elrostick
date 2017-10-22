
ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

MAINTAINER mgolisch
LABEL Name=Flask-Elrostick Version=0.0.1 
RUN apk update && apk add jq python py2-pip py2-pysqlite bash
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD sh run_hassio.sh
