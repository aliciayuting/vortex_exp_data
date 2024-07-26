#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: No directory to store exp data provided."
  echo "Usage: $0 <local_directory>"
  exit 1
fi

# Assign the first argument to local_directory
local_directory="$1"


ips=("192.168.99.30" "192.168.99.32" "192.168.99.31")
node_names=("compute30" "compute32" "compute31")
# ips=("compute25" "compute32" "compute31" "compute30" "compute29" "compute28" "compute26")
node_ids=("n0" "n1" "n2")

file_suffix=".dat"

remote_directory="~/workspace/cascade/build-Release/src/applications/rag_demo/cfg"

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
remote_perf_config_dir="~/workspace/cascade/build-Release/src/applications/rag_demo/cfg/${node_ids[0]}/perf_test/perf_config.py"
scp "${node_names[0]}:${remote_perf_config_dir}" "${local_directory}/"