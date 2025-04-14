#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: No directory to store exp data provided."
  echo "Usage: $0 <local_directory>"
  exit 1
fi

# Assign the first argument to local_directory
local_directory="$1"


node_names=("TY373@d7525-10s10311.wisc.cloudlab.us" \
            "TY373@d7525-10s10325.wisc.cloudlab.us" \
            "TY373@d7525-10s10321.wisc.cloudlab.us" \
            "TY373@d7525-10s10331.wisc.cloudlab.us"\
            "TY373@d7525-10s10331.wisc.cloudlab.us"\
            "TY373@d7525-10s10331.wisc.cloudlab.us"\
            "TY373@d7525-10s10331.wisc.cloudlab.us"\
            "TY373@d7525-10s10319.wisc.cloudlab.us")

node_ids=("n0" "n1" "n2" "n3" "n4" "n5" "n6" "n7")
# ips=("192.168.9.30" "192.168.9.32" "192.168.9.31")
# node_names=("compute30" "compute32" "compute31")
# node_ids=("n0" "n1" "n2")

file_suffix=".csv"

remote_directory="~/workspace/torchServVortexppl/"

for ((i=0; i<${#node_names[@]}; i++)); do
     node_name="${node_names[i]}"
     node_id="${node_ids[i]}"
     # create local directory to store data from that node
     mkdir -p "${local_directory}/${node_id}"
     files=$(ssh "$node_name" "find ${remote_directory} -type f -name '*${file_suffix}'")
     # Copy data from remote to local
     for file in $files; do
          scp "${node_name}:${file}" "${local_directory}/${node_id}"
     done
done

