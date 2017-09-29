# This Dockerfile is based off the Google App Engine Python runtime image
# https://github.com/GoogleCloudPlatform/python-runtime
FROM uccser/python:3.6.2-stretch-with-weasyprint

# Add metadata to Docker image
LABEL maintainer="csse-education-research@canterbury.ac.nz"

# Set terminal to be noninteractive
ARG DEBIAN_FRONTEND=noninteractive
ARG PROCESS_PORT=8080
ARG FLASK_PRODUCTION=1
ARG PROJECT_NAME=cs-unplugged
ARG QUEUE_NAME=render-queue
ARG API_DISCOVERY_URL
ARG BUCKET_NAME=cs-unplugged-dev.appspot.com
ARG STATIC_DIRECTORY=/renderservice/static_mnt

ENV PORT ${PROCESS_PORT}
ENV FLASK_PRODUCTION ${FLASK_PRODUCTION}
ENV PROJECT_NAME ${PROJECT_NAME}
ENV QUEUE_NAME ${QUEUE_NAME}
ENV API_DISCOVERY_URL ${API_DISCOVERY_URL}
ENV STATIC_DIRECTORY ${STATIC_DIRECTORY}
ENV CLOUD_STORAGE_BUCKET_NAME ${BUCKET_NAME}
ENV GOOGLE_CLOUD_BUCKET_KEY /keys/bucket.json
ENV GOOGLE_APPLICATION_CREDENTIALS /keys/compute.json

# Install GCSFUSE
RUN apt-get update \
    && apt-get install -y lsb-release kmod \
    && export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s` \
    && echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | tee /etc/apt/sources.list.d/gcsfuse.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && apt-get update \
    && apt-get install -y \
      gcsfuse \
    && apt-get clean && rm /var/lib/apt/lists/*_*

# Set-up file system
RUN mkdir /renderservice
RUN mkdir /renderservice/scripts
RUN mkdir /keys
COPY requirements.txt /renderservice
COPY bucket.json /keys/bucket.json
COPY compute.json /keys/compute.json

# Install dependencies
RUN /docker_venv/bin/pip3 install -r /renderservice/requirements.txt

# Setup Working Directory
ADD . /renderservice
WORKDIR /renderservice

# Setup User
RUN useradd -c "RenderService user" -m -d /home/render -s /bin/bash render \
    && chown -R render /renderservice \
    && mkdir ${STATIC_DIRECTORY} \
    && chown -R render ${STATIC_DIRECTORY}
USER render
ENV HOME /home/render

EXPOSE ${PORT}

# Run System
RUN chmod +x /renderservice/scripts/mount-bucket.sh
RUN chmod +x /renderservice/scripts/docker-entrypoint.sh
RUN chmod +x /renderservice/scripts/deploy-docker-entrypoint.sh
ENTRYPOINT ["/renderservice/scripts/deploy-docker-entrypoint.sh"]
