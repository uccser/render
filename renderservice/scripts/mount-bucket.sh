#!/bin/bash
BUCKET_NAME=$1
DIRECTORY=$2

if [ ! -d "${DIRECTORY}" ]; then
  mkdir ${DIRECTORY}
fi

gcsfuse --key-file ${GOOGLE_CLOUD_BUCKET_KEY} ${BUCKET_NAME} ${DIRECTORY}
