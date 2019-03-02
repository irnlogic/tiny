#FROM python:3.6.7-alpine
#FROM python:3-alpine
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD src/ /code/
ENTRYPOINT python tinyapp/manage.py makemigrations
ENTRYPOINT python tinyapp/manage.py migrate
ENTRYPOINT ["python", "tinyapp/manage.py", "runserver", "0.0.0.0:8001"]

