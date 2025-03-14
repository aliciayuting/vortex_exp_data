#!/bin/bash



# 1. create configuration files for each node
# 1.1. Write to local directory
local_cfg_directory="./cfg"
derecho_cfg_file_name="derecho.cfg"
env_file_name="set_nv_env.sh"
dfgs_file="dfgs.json.tmp"
gpu_monitor_file="gpu_monitor.sh"
ab_client_py="stepABclient.py"
dfgs_file_path="${local_cfg_directory}/${dfgs_file}"

ips=("10.10.1.1"\
     "10.10.1.2"\
     "10.10.1.6" \
     "10.10.1.6" \
     "10.10.1.4"\
     "10.10.1.4"\
     "10.10.1.5")
#     "10.10.1.4"\
#     "10.10.1.5"\
#     "10.10.1.6"\
#     "10.10.1.7"\
#     "10.10.1.8"\
#     "10.10.1.9")
node_names=("TY373@d7525-10s10311.wisc.cloudlab.us" \
            "TY373@d7525-10s10325.wisc.cloudlab.us" \
            "TY373@d7525-10s10321.wisc.cloudlab.us" \
            "TY373@d7525-10s10321.wisc.cloudlab.us" \
            "TY373@d7525-10s10331.wisc.cloudlab.us"\
            "TY373@d7525-10s10331.wisc.cloudlab.us"\
            "TY373@d7525-10s10319.wisc.cloudlab.us")
          #   "Alicia@d7525-10s10339.wisc.cloudlab.us"\
          #   "Alicia@d7525-10s10315.wisc.cloudlab.us"\
          #   "Alicia@d7525-10s10327.wisc.cloudlab.us"\
          #   "Alicia@d7525-10s10333.wisc.cloudlab.us"\
          #   "Alicia@d7525-10s10329.wisc.cloudlab.us"\
          #   "Alicia@d7525-10s10317.wisc.cloudlab.us")
node_ids=("n0" "n1" "n2" "n3" "n4" "n5" "n6")
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

     env_file_path="${local_cfg_directory}/${node_id}/${env_file_name}"
     scp "${env_file_path}" "${node_name}:${remote_cfg_directory}/${node_id}/"

     gpu_monitor_file_path="${local_cfg_directory}/${gpu_monitor_file}"
     scp "${gpu_monitor_file_path}" "${node_name}:${remote_cfg_directory}/${node_id}/"

     layot_file_path="${local_cfg_directory}/layout.json"
     scp "${layot_file_path}" "${node_name}:${remote_cfg_directory}/${node_id}/"

     dfgs_file_path="${local_cfg_directory}/${dfgs_file}"
     scp "${dfgs_file_path}" "${node_name}:${remote_cfg_directory}/"
     sleep 1
done

last_node_id=${node_ids[${#node_ids[@]}-1]}
last_remote_node_name=${node_names[${#node_names[@]}-1]}
ab_client_file_path="${local_cfg_directory}/${ab_client_py}"
scp "${ab_client_file_path}" "${last_remote_node_name}:${remote_cfg_directory}/${last_node_id}/pipeline_client/"