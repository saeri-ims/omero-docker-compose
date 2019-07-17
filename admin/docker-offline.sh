#!/bin/bash

set -eu
IMAGES=(
    postgres:9.6
    openmicroscopy/omero-server:5.5.0
    openmicroscopy/omero-web-standalone:5.5.0
)

usage() {
    echo "USAGE: $(basename $0) [save|load]"
    exit 1
}
if [ $# -ne 1 ]; then
    usage
fi

for im in "${IMAGES[@]}"; do
    imtar="$(echo "$im" | tr -cd '[:alnum:]._-').tar"
    if [ "$1" = "save" ]; then
        docker pull "$im"
        echo "Saving $im to $imtar"
        docker save "$im" > "$imtar"
    elif [ "$1" = "load" ]; then
        echo "Loading $im from $imtar"
        docker load < "$imtar"
    else
        usage
    fi
done
