FROM python:3.6.8

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
COPY ./requirements.txt /code

WORKDIR /code

RUN sed -i "s/archive.ubuntu./mirrors.aliyun./g" /etc/apt/sources.list
RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list

RUN apt-get clean && apt-get -y update && \
    apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev libsnmp-dev

RUN pip3 install -r requirements.txt

COPY ./* /code/