#!/bin/bash

# NOTE: Changes in rag_demo/cfg/ is not reflected here, since we use local stored cfgs. 
# Copy the files here if need the updated cfgs.



echo "search_type: 0: CPU flat search, 1: GPU flat search, 2: GPU IVF search"
read search_type

echo "TOTAL_BATCH_COUNT:"
read total_batch_count

echo "QUERY_PER_BATCH:"
read query_per_batch

# 1. create configuration files for each node
# 1.1. Write to local directory
local_directory="./exp_data"
local_cfg_directory="${local_directory}/cfg"
derecho_cfg_file_name="derecho.cfg"

ips=("192.168.9.30" "192.168.9.32" "192.168.9.31")
node_names=("compute30" "compute32" "compute31")
node_ids=("n0" "n1" "n2" )
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



perf_config_file="perf_config.py"
perf_config_file_path="${local_cfg_directory}/${perf_config_file}"
line_numbers=(17 18)
batch_count_sentence="TOTAL_BATCH_COUNT = ${total_batch_count}"
sed "${line_numbers[0]}s/.*/${batch_count_sentence}/" "${perf_config_file_path}" > "${perf_config_file_path}.tmp"
mv "${perf_config_file_path}.tmp" "${perf_config_file_path}"
query_per_batch_sentence="QUERY_PER_BATCH = ${query_per_batch}"
sed "${line_numbers[1]}s/.*/${query_per_batch_sentence}/" "${perf_config_file_path}" > "${perf_config_file_path}.tmp"
mv "${perf_config_file_path}.tmp" "${perf_config_file_path}"

dfgs_file="dfgs.json.tmp"
dfgs_file_path="${local_cfg_directory}/${dfgs_file}"
line_numbers=(16 29)
centroid_search_type_sentence="                        \"faiss_search_type\":${search_type}"
sed "${line_numbers[0]}s/.*/${centroid_search_type_sentence}/" "${dfgs_file_path}" > "${dfgs_file_path}.tmp"
mv "${dfgs_file_path}.tmp" "${dfgs_file_path}"
cluster_search_type_sentence="                        \"faiss_search_type\":${search_type}"
sed "${line_numbers[1]}s/.*/${cluster_search_type_sentence}/" "${dfgs_file_path}" > "${dfgs_file_path}.tmp"
mv "${dfgs_file_path}.tmp" "${dfgs_file_path}"

# 2. scp to remote directory

remote_cfg_directory="~/workspace/cascade/build-Release/src/applications/rag_demo/cfg"
remote_perfconfig_directory="~/workspace/cascade/build-Release/src/applications/rag_demo/perf_test"
for ((i=0; i<${#ips[@]}; i++)); do
     node_name="${node_names[i]}"
     node_id="${node_ids[i]}"
     cfg_file_path="${local_cfg_directory}/${node_id}/${derecho_cfg_file_name}"
     scp "${cfg_file_path}" "${node_name}:${remote_cfg_directory}/${node_id}/" 
     perf_config_file_path="${local_cfg_directory}/${perf_config_file}"
     scp "${perf_config_file_path}" "${node_name}:${remote_perfconfig_directory}/"
     dfgs_file_path="${local_cfg_directory}/${dfgs_file}"
     scp "${dfgs_file_path}" "${node_name}:${remote_cfg_directory}/"
     layot_file_path="${local_cfg_directory}/layout.json.tmp"
     scp "${layot_file_path}" "${node_name}:${remote_cfg_directory}/"
done

