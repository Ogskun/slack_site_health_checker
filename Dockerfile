FROM --platform=linux/amd64 ubuntu:jammy
RUN apt update -y
RUN apt upgrade -y
RUN apt install gcc python3-dev python3-pip -y
ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
WORKDIR /app
EXPOSE 8080