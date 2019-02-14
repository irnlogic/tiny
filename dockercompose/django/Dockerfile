#FROM python:3.6.7-alpine
#FROM python:3-alpine
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD src/ /code/
CMD python tinyapp/manage.py makemigrations
CMD python tinyapp/manage.py migrate
CMD ["python", "tinyapp/manage.py", "runserver", "0.0.0.0:8001"]

