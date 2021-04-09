FROM ubuntu:18.04

MAINTAINER Vladimir Visnovsky "467814@muni.cz"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN bash -c "apt-get install vim -y"

ENV OAUTHLIB_INSECURE_TRANSPORT=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY app/ /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["/bin/sh -c 'while true; do sleep 10;done'"]
