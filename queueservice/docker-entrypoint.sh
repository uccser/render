#!/bin/bash
export NETWORK_IPADDRESS=`awk 'END{print $1}' /etc/hosts`
echo 'export NETWORK_IPADDRESS=${NETWORK_IPADDRESS}' >> ~/.bashrc
/docker_venv/bin/gunicorn -c ./gunicorn.conf.py -b :${PORT} wsgi
