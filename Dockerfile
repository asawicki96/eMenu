FROM python:3.8


COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./ /app/

RUN mkdir -p /vol/backend/media
RUN mkdir -p /vol/web/static

RUN chmod -R 755 /vol/backend


