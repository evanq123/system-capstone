# Dockerfile for app image
FROM centos/python-36-centos7

RUN pip3 install -r requirements.txt

COPY Makefile .local_config.yaml app.py ./
COPY tests ./tests
COPY scripts ./scripts
COPY src ./src
