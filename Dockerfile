FROM python:3.11-alpine

ADD ./ /app
WORKDIR /app

RUN set -ex \
    && apk add --no-cache --virtual .build-deps build-base \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && mkdir export \
    && apk del .build-deps

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

RUN set -ex \
    && python manage.py collectstatic --noinput \
    && python manage.py makemigrations \
    && python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "StatTrackingBackend.wsgi:application"]