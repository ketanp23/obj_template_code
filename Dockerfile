#FROM ubuntu:20.04
#FROM spmallick/opencv-docker:opencv

FROM jjanzic/docker-python3-opencv:latest
#FROM ulikoehler/ubuntu-python3-opencv:latest

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update -y && apt-get install wget -y
#&& apt-get install -y python3-pip
#RUN pip3 install cvlib
#libgl1 libglib2.0-0

# We copy just the requirements.txt first to leverage Docker cache
ADD requirements.txt /app/

WORKDIR /app


RUN /bin/bash -c "pip3 install --no-cache-dir -r requirements.txt"

ADD /app/ /app/

RUN wget https://pjreddie.com/media/files/yolov3.weights

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]