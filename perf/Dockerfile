FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD test.py /code/
#CMD ["test.py", "-c", "200", "1", "100"]
CMD python test.py -c 200 1 1

