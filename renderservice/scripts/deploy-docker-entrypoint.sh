#!/bin/bash
source /renderservice/scripts/mount-bucket.sh ${CLOUD_STORAGE_BUCKET_NAME} ${STATIC_DIRECTORY}
source /renderservice/scripts/docker-entrypoint.sh
