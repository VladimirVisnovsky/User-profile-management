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

name="spectraes/user-profile-management:$(date +%F)${id}"
build="${application} build -t ${name} ."
push="${application} push ${name}"

echo "$name" > latest-image.txt
eval "${build} && ${push}"

if [[ $? == 0 ]]; then
        echo "successfully built and pushed image ${name}"
fi
