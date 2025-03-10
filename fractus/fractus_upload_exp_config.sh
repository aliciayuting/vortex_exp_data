#!/bin/bash



# 1. create configuration files for each node
# 1.1. Write to local directory
local_cfg_directory="./cfg"
derecho_cfg_file_name="derecho.cfg"
dfgs_file="dfgs.json.tmp"
dfgs_file_path="${local_cfg_directory}/${dfgs_file}"

ips=("192.168.9.32" "192.168.9.30" "192.168.9.28" "192.168.9.29")
node_names=("compute32" "compute30" "compute28" "compute29")
node_ids=("n0" "n1" "n2" "n3" )
#  "n3" "n4" "n5" "n6" "n7" "n8")

line_numbers=(3 9)
for ((i=0; i<${#node_ids[@]}; i++)); do
     file_path="${local_cfg_directory}/${node_ids[i]}/${derecho_cfg_file_name}"
     contact_ip_sentence="contact_ip = ${ips[0]}"
     sed "${line_numbers[0]}s/.*/${contact_ip_sentence}/" "${file_path}" > "${file_path}.tmp"
     mv "${file_path}.tmp" "${file_path}"
     local_ip_sentence="local_ip = ${ips[i]}"
     sed "${line_numbers[1]}s/.*/${local_ip_sentence}/" "${file_path}" > "${file_path}.tmp"
     mv "${file_path}.tmp" "${file_path}"
done




# 2. scp to remote directory

remote_cfg_directory="~/workspace/vortex_udlppl1/build-Release/cfg"

for ((i=0; i<${#ips[@]}; i++)); do
     node_name="${node_names[i]}"
     node_id="${node_ids[i]}"
     cfg_file_path="${local_cfg_directory}/${node_id}/${derecho_cfg_file_name}"
     scp "${cfg_file_path}" "${node_name}:${remote_cfg_directory}/${node_id}/" 
     layot_file_path="${local_cfg_directory}/layout.json"
     scp "${layot_file_path}" "${node_name}:${remote_cfg_directory}/${node_id}/"
     dfgs_file_path="${local_cfg_directory}/${dfgs_file}"
     scp "${dfgs_file_path}" "${node_name}:${remote_cfg_directory}/"
done
