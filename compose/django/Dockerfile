FROM python:3.5

ENV PYTHONUNBUFFERED 1

ADD requirements /tmp/
WORKDIR /tmp/
RUN pip install -r local.txt

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/django/start-dev.sh /start-dev.sh
RUN sed -i 's/\r//' /start-dev.sh
RUN chmod +x /start-dev.sh

ENV APPLICATION_ROOT /app
RUN mkdir -p $APPLICATION_ROOT

WORKDIR $APPLICATION_ROOT/sample_django_app
