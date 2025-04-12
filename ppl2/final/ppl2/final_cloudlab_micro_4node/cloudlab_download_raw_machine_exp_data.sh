#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: No directory to store exp data provided."
  echo "Usage: $0 <local_directory>"
  exit 1
fi

# Assign the first argument to local_directory
local_directory="$1"


node_names=("TY373@d7525-10s10323.wisc.cloudlab.us" \
            "TY373@d7525-10s10323.wisc.cloudlab.us" \
            "TY373@d7525-10s10327.wisc.cloudlab.us" \
            "TY373@d7525-10s10327.wisc.cloudlab.us" \
            "TY373@d7525-10s10321.wisc.cloudlab.us" \
            "TY373@d7525-10s10321.wisc.cloudlab.us" \
            "TY373@d7525-10s10329.wisc.cloudlab.us"\
            "TY373@d7525-10s10329.wisc.cloudlab.us"\
            "TY373@d7525-10s10335.wisc.cloudlab.us")

node_ids=("n0" "n1" "n2" "n3" "n4" "n5" "n6" "n7" "n8")
file_suffix=".dat"

remote_directory="~/workspace/vortex/build-Release/cfg"

for ((i=0; i<${#node_names[@]}; i++)); do
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
scp "${node_names[0]}:${remote_directory}/dfgs.json.tmp" "${local_directory}/"


# Copy client to local file
last_node_id=${node_ids[${#node_ids[@]}-1]}
last_remote_node_name=${node_names[${#node_names[@]}-1]}

# read -p "Is this a mono client? [y/N]: " is_mono
# if [[ "$is_mono" =~ ^[Yy] ]]; then
#     remote_mono_client="~/workspace/vortex_udlppl1/build-Release/cfg/${last_node_id}/pipeline_client/monoClient.py"
#     scp "${last_remote_node_name}:${remote_mono_client}" "${local_directory}/"
# else
remote_perf_client="~/workspace/vortex/build-Release/cfg/${last_node_id}/pipeline_client/ppl2_client.py"
scp "${last_remote_node_name}:${remote_perf_client}" "${local_directory}/"
# fi

# Copy server config to local file
remote_layout_dir="~/workspace/vortex/build-Release/cfg/layout.json.tmp"
scp "${node_names[0]}:${remote_layout_dir}" "${local_directory}/"