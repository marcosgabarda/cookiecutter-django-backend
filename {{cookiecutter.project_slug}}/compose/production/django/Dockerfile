FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi

{% if cookiecutter.use_postgis == 'y' -%}
 # GeoDjango Support
RUN apk add --update alpine-sdk

ENV CFLAGS="$CFLAGS -L/lib"
RUN apk update && \
    apk upgrade && \
    apk add --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
     --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
     --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/community \
     bash \
     binutils \
     gcc \
     gdal \
     gdal-dev \
     py-gdal \
     geos \
     git \
     libpq \
     linux-headers \
     mailcap \
     proj4-dev \
     postgresql && \
    rm -rf /var/cache/apk/*
RUN ln -s /usr/lib/libgeos_c.so.1 /usr/local/lib/libgeos_c.so
{%- endif %}

RUN addgroup -S django \
    && adduser -S -G django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start
{% if cookiecutter.use_celery == "y" %}
COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

COPY ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown django /start-celerybeat

COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower
{% endif %}
COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
