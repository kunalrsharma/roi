FROM ubuntu:latest 

RUN apt update && apt install -y python3 python3-pip 
RUN pip3 install Django 

ADD ./mysite . 

EXPOSE 8000

CMD python3 manage.py runserver



