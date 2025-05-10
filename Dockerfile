FROM python:3.12

COPY scripts /scripts
COPY requirements.txt /requirements.txt
COPY entry.sh /entry.sh

RUN pip install -r /requirements.txt