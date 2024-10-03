FROM python:3.9-bullseye as base

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ENV STATIC_ROOT /static
ENV MEDIA_ROOT /media

ENV _UWSGI_VERSION 2.0.18
ENV DOCKERIZE_VERSION v0.6.1
ENV WKHTMLTOPDF_VERSION 0.12.3

VOLUME /static
VOLUME /media

EXPOSE 8000

RUN apt-get update \
    && apt-get --no-install-recommends install -y gettext locales-all wget imagemagick tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get --no-install-recommends install -y build-essential libxml2-dev libxslt1-dev \
    && apt-get --no-install-recommends install -y libjpeg62-turbo-dev libjpeg-dev libfreetype6-dev libtiff5-dev liblcms2-dev libwebp-dev tk8.6-dev \
    && apt-get --no-install-recommends install -y libffi-dev libcgraph6 libgraphviz-dev libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN wget -O uwsgi-${_UWSGI_VERSION}.tar.gz https://github.com/unbit/uwsgi/archive/${_UWSGI_VERSION}.tar.gz \
    && tar zxvf uwsgi-*.tar.gz \
    && UWSGI_BIN_NAME=/usr/local/bin/uwsgi make -C uwsgi-${_UWSGI_VERSION} \
    && rm -Rf uwsgi-*

ENV ON_BUILD_ENV_FILE=.env.ci

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /srv
ADD . /srv/

RUN ENV_FILE=$ON_BUILD_ENV_FILE ./manage.py compilemessages

FROM base as backend

CMD uwsgi --http :8000 --module app.wsgi --workers 2 --threads 2 --harakiri 40 --max-requests 500 --buffer-size 65545


FROM base as celery
ENV QUEUE=default

CMD celery -A app worker -Q $QUEUE -c ${CONCURENCY:-2} -n "${QUEUE}@%h" --max-tasks-per-child ${MAX_REQUESTS_PER_CHILD:-50} --time-limit ${TIME_LIMIT:-900} --soft-time-limit ${SOFT_TIME_LIMIT:-45}
