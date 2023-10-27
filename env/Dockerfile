FROM python:3.10
RUN apt-get update && apt-get install -y \
    build-essential \
    git 
WORKDIR /code
RUN pip install --upgrade pip
COPY env/requirements.txt env/requirements.txt
RUN pip install wheel rpi-gpio spidev
RUN pip install -r env/requirements.txt
ENV PYTHONUNBUFFERED=1