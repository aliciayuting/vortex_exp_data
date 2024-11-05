#!/bin/bash

# NOTE: Changes in rag_demo/cfg/ is not reflected here, since we use local stored cfgs. 
# Copy the files here if need the updated cfgs.



echo "centroids_search_type: 0: CPU flat search, 1: GPU flat search, 2: GPU IVF search"
read centroids_search_type

echo "cluster_search_type: 0: CPU flat search, 1: GPU flat search, 2: GPU IVF search"
read cluster_search_type

echo "USE_OPENAI_API: true/false"   
read use_openai_api

echo "RETRIEVE_DOC: true/false"   
read retrieve_doc_setting

echo "TOTAL_BATCH_COUNT:"
read total_batch_count

echo "QUERY_PER_BATCH:"
read query_per_batch

echo "QUERY_INTERVAL(us):"
read query_interval

echo "DATA_SET:"
read data_set

echo "EMB_DIM:"
read dim


# 1. create configuration files for each node
# 1.1. Write to local directory
local_directory="./exp_data"
local_cfg_directory="${local_directory}/cfg"
derecho_cfg_file_name="derecho.cfg"

ips=("192.168.9.30" "192.168.9.32" "192.168.9.29" "192.168.9.31" "192.168.9.28")
node_names=("compute30" "compute32" "compute29" "compute31" "compute28")
node_ids=("n0" "n1" "n2" "n3" "n4")
# ips=("192.168.9.29" "192.168.9.31" "192.168.9.28" )
# node_names=("compute29"  "compute31" "compute28")
# node_ids=("n0" "n1" "n2")
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


data_set_dir="perf_data/${data_set}"
run_client_file="run_client.sh"

run_command="./latency_client -n ${total_batch_count} -b ${query_per_batch} -q ${data_set_dir} -i ${query_interval} -e ${dim}"
if [ "$use_openai_api" = "true" ]; then
    run_command+=" -t"
fi
echo "${run_command}" > "${local_cfg_directory}/${run_client_file}"

run_client_init_file="run_init.sh"
run_command="python setup/perf_test_setup.py -p ${data_set_dir} -e ${dim}"
if [ "$retrieve_doc_setting" = "true" ]; then
    run_command+=" -doc"
fi
echo "${run_command}" > "${local_cfg_directory}/${run_client_init_file}"

dfgs_file="dfgs.json.tmp"
dfgs_file_path="${local_cfg_directory}/${dfgs_file}"
line_numbers=(16 33 14 31 47 17 46)

centroid_search_type_sentence="                        \"faiss_search_type\":${centroids_search_type},"
sed "${line_numbers[0]}s/.*/${centroid_search_type_sentence}/" "${dfgs_file_path}" > "${dfgs_file_path}.tmp"
mv "${dfgs_file_path}.tmp" "${dfgs_file_path}"
cluster_search_type_sentence="                        \"faiss_search_type\":${cluster_search_type}"
sed "${line_numbers[1]}s/.*/${cluster_search_type_sentence}/" "${dfgs_file_path}" > "${dfgs_file_path}.tmp"
mv "${dfgs_file_path}.tmp" "${dfgs_file_path}"
emb_dim_sentence="                        \"emb_dim\":${dim},"
sed "${line_numbers[2]}s/.*/${emb_dim_sentence}/" "${dfgs_file_path}" > "${dfgs_file_path}.tmp"
mv "${dfgs_file_path}.tmp" "${dfgs_file_path}"
sed "${line_numbers[3]}s/.*/${emb_dim_sentence}/" "${dfgs_file_path}" > "${dfgs_file_path}.tmp"
mv "${dfgs_file_path}.tmp" "${dfgs_file_path}"
retrieve_doc_setting_sentence="                        \"retrieve_docs\":${retrieve_doc_setting},"
sed "${line_numbers[4]}s/.*/${retrieve_doc_setting_sentence}/" "${dfgs_file_path}" > "${dfgs_file_path}.tmp"
mv "${dfgs_file_path}.tmp" "${dfgs_file_path}"
include_encoder_sentence="                        \"include_encoder\":${use_openai_api},"
sed "${line_numbers[5]}s/.*/${include_encoder_sentence}/" "${dfgs_file_path}" > "${dfgs_file_path}.tmp"
mv "${dfgs_file_path}.tmp" "${dfgs_file_path}"
include_llm_sentence="                        \"include_llm\":${use_openai_api},"
sed "${line_numbers[6]}s/.*/${include_llm_sentence}/" "${dfgs_file_path}" > "${dfgs_file_path}.tmp"
mv "${dfgs_file_path}.tmp" "${dfgs_file_path}"



# 2. scp to remote directory

remote_cfg_directory="~/workspace/vortex/build-Release/cfg"
for ((i=0; i<${#ips[@]}; i++)); do
     node_name="${node_names[i]}"
     node_id="${node_ids[i]}"
     cfg_file_path="${local_cfg_directory}/${node_id}/${derecho_cfg_file_name}"
     scp "${cfg_file_path}" "${node_name}:${remote_cfg_directory}/${node_id}/" 
     run_client_file_path="${local_cfg_directory}/${run_client_file}"
     scp "${run_client_file_path}" "${node_name}:${remote_cfg_directory}/${node_id}/"
     run_init_file_path="${local_cfg_directory}/${run_client_init_file}"
     scp "${run_init_file_path}" "${node_name}:${remote_cfg_directory}/${node_id}/"
     dfgs_file_path="${local_cfg_directory}/${dfgs_file}"
     scp "${dfgs_file_path}" "${node_name}:${remote_cfg_directory}/"
     layot_file_path="${local_cfg_directory}/layout.json.tmp"
     scp "${layot_file_path}" "${node_name}:${remote_cfg_directory}/"
done

