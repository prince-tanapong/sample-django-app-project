FROM python:2.7

ADD requirements /tmp/
WORKDIR /tmp/
RUN pip install -r local.txt

ENV APPLICATION_ROOT /app
RUN mkdir -p $APPLICATION_ROOT
WORKDIR $APPLICATION_ROOT
ADD . $APPLICATION_ROOT

WORKDIR $APPLICATION_ROOT/sample_django_app
