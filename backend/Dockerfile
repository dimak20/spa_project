FROM python:3.11.6-alpine3.18
LABEL maintainer="dima.kolhac@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

RUN chown -R my_user /files/media
RUN chmod -R 755 /files/media

RUN python manage.py collectstatic --noinput || true

USER my_user

CMD ["uvicorn", "spa_app.asgi:application", "--host", "0.0.0.0", "--port", "8000"]