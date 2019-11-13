FROM python:3.7

WORKDIR /app

COPY . /app

RUN pip install flask requests lxml

EXPOSE 80

CMD python ./webserver.py
