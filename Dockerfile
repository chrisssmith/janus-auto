FROM ubuntu:16.04

RUN apt-get update
RUN apt-get update 
RUN apt-get install tesseract-ocr -y
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

RUN echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.0.list 
RUN apt-get update && apt-get install -y mongodb-org 
RUN cd /etc/systemd/system/
RUN touch mongodb.service
RUN echo "[Unit]" | tee -a mongodb.service
RUN echo "Description=High-performance, schema-free document-oriented database" | tee -a mongodb.service
RUN echo "After=network.target" | tee -a mongodb.service
RUN echo "" | tee -a mongodb.service
RUN echo "[Service]" | tee -a mongodb.service
RUN echo "User=mongodb" | tee -a mongodb.service
RUN echo "ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf" | tee -a mongodb.service
RUN echo "" | tee -a mongodb.service
RUN echo "[Install]" | tee -a mongodb.service
RUN echo "WantedBy=multi-user.target" | tee -a mongodb.service
RUN cd
RUN apt-get install python-pip python-dev build-essential -y
RUN pip install --upgrade pip 
RUN pip install --upgrade virtualenv 
RUN apt-get update 
