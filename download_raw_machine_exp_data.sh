#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: No directory to store exp data provided."
  echo "Usage: $0 <local_directory>"
  exit 1
fi

# Assign the first argument to local_directory
local_directory="$1"


ips=("192.168.9.30" "192.168.9.32" "192.168.9.29" "192.168.9.31" "192.168.9.28")
node_names=("compute30" "compute32" "compute29" "compute31" "compute28")
node_ids=("n0" "n1" "n2" "n3" "n4")
# ips=("192.168.9.30" "192.168.9.32" "192.168.9.31")
# node_names=("compute30" "compute32" "compute31")
# node_ids=("n0" "n1" "n2")

file_suffix=".dat"

remote_directory="~/workspace/vortex/build-Release/cfg"

for ((i=0; i<${#ips[@]}; i++)); do
     node_name="${node_names[i]}"
     node_id="${node_ids[i]}"
     # create local directory to store data from that node
     mkdir -p "${local_directory}/${node_id}"
     files=$(ssh "$node_name" "find ${remote_directory}/${node_id} -type f -name '*${file_suffix}'")
     # Copy data from remote to local
     for file in $files; do
          scp "${node_name}:${file}" "${local_directory}/${node_id}"
     done
done

# Copy config to local file
scp "${node_name}:${remote_directory}/dfgs.json.tmp" "${local_directory}/"
# Copy client config to local file
remote_perf_config_dir="~/workspace/vortex/build-Release/cfg/${node_ids[0]}/run_client.sh"
scp "${node_names[0]}:${remote_perf_config_dir}" "${local_directory}/"
# Copy server config to local file
remote_layout_dir="~/workspace/vortex/build-Release/cfg/layout.json.tmp"
scp "${node_names[0]}:${remote_layout_dir}" "${local_directory}/"