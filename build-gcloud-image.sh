#!/bin/bash
set -e

function get_render_version(){
render_version=`python3 -c 'from renderservice.render import __version__;print(__version__)'`
}

host="gcr.io"
project_id="render-181102"
username="uccser"
get_render_version

docker build renderservice -t "${host}/${project_id}/${username}/render:${render_version}"
gcloud docker -- push "${host}/${project_id}/${username}/render:${render_version}"
