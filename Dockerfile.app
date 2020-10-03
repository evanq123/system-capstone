# Dockerfile for app image
FROM centos/python-36-centos7


COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY Makefile app.py ./
COPY tests ./tests
COPY scripts ./scripts
COPY src ./src
