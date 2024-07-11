#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: No directory provided."
  echo "Usage: $0 <local_directory>"
  exit 1
fi

# Assign the first argument to local_directory
local_directory="$1"


ips=("compute28")
# ips=("compute25" "compute32" "compute31" "compute30" "compute29" "compute28" "compute26")

file_suffix=".dat"

remote_directory="~/rag_exp_results"


for ((i=0; i<${#ips[@]}; i++)); do
     ip="${ips[i]}"
     files=$(ssh "$ip" "find ${remote_directory} -type f -name '*${file_suffix}'")
     # Copy files from remote to local
     for file in $files; do
          scp "${ip}:${file}" "${local_directory}/${exp_name}/${node_id}"
     done
     # # GPU tracking data download
     # if [[ "${download_gpu}" == "y" ]]; then
     #      scp "${ip}:~/gpu_utilizations.csv" "${local_directory}/${node_id}"
     #      scp "${ip}:~/gpu_memories.csv" "${local_directory}/${node_id}"
     # fi
done