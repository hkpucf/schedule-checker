FROM python:2.7

WORKDIR /app

COPY . /app

RUN pip install requests lxml

EXPOSE 80

CMD python ./webserver.py
