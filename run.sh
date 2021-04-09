#!/bin/bash

unset id
application="docker"

while getopts ":pi:" opt; do
  case $opt in
    p)
      application="podman"
      echo "building with podman.." >&2
      ;;
    i)
      id="-${OPTARG}"
      echo "building with id $id"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done


source secrets.sh
name=$(head -n 1 latest-image.txt)
docker run -p 5000:5000 -e GOOGLE_ID=${ID} -e GOOGLE_SECRET=${SECRET} -v $PWD/app/work:/app/work -ti ${name} bash

