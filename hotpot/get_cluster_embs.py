from hotpot_preprocess import *
import pickle

import os
import shutil
from collections import defaultdict

CLUSTER_NUM = 15



def create_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted existing folder: {folder_path}")
    os.makedirs(folder_path)
    print(f"Created new folder: {folder_path}")


def put_centroids_to_folder(folder_path):
    with open(f'cluster/hotpot_centroids_{CLUSTER_NUM}.pkl', 'rb') as f:
        centroids = pickle.load(f)
    print(f"Centroids shape: {centroids.shape}")
    with open(f'{folder_path}/centroids.pkl', 'wb') as f:
        pickle.dump(centroids, f)


def get_embs_by_cluster():
    I = []
    with open(f'cluster/hotpot_index_{CLUSTER_NUM}.pkl', 'rb') as f:
        I = pickle.load(f)
    
    doc_emb_map = defaultdict(dict)
    clustered_embs = [[] for _ in range(CLUSTER_NUM)]
    with open('hotpot_train_v1.1_full_emb3small.pkl', 'rb') as f:
        embs = pickle.load(f)
        for i in range(len(embs)):
            cluster = I[i][0]
            if len(I[i]) != 1:
                print(f"Error in embedding {i}, len {len(I[i])}")
            clustered_embs[cluster].append(embs[i])
            emb_id = len(clustered_embs[cluster]) - 1
            doc_emb_map[cluster][emb_id] = i
    return clustered_embs, doc_emb_map


def write_cluster_embs(clustered_embs,folder_path):
    for i, cluster in enumerate(clustered_embs):
        with open(f'{folder_path}/cluster_{i}.pkl', 'wb') as f:
            pickle.dump(cluster, f)

def write_doc_emb_map(doc_emb_map,folder_path):
    with open(f'{folder_path}/doc_emb_map.pkl', 'wb') as f:
        pickle.dump(doc_emb_map, f)

def copy_doc_list(folder_path):
    # copy the file hotpot_context.pkl to the folder with new name dock_list.pkl
    shutil.copyfile('hotpot_context.pkl', f'{folder_path}/doc_list.pkl')


def sanity_check(doc_emb_map, doc_list_pathname):
    with open(doc_list_pathname, 'rb') as f:
        doc_list = pickle.load(f)
    total_num_embs = 0
    for cluster in doc_emb_map:
        total_num_embs += len(doc_emb_map[cluster])
    if len(doc_list) != total_num_embs:
        print(f"Error: doc_list has {len(doc_list)} embeddings, but doc_emb_map has {total_num_embs} embeddings")
    else:
        print(f"Sanity check passed: doc_list has {len(doc_list)} embeddings, and doc_emb_map has {total_num_embs} embeddings")

def copy_question_json():
    shutil.copyfile('hotpot_train_v1.1_questions_1500.json', f'cluster/hotpot{CLUSTER_NUM}/question_emb.json')


if __name__ == "__main__":
    # # create a folder under cluster/CLUSTER_NUM
    # create_folder(f'cluster/hotpot{CLUSTER_NUM}')
    # put_centroids_to_folder(f'cluster/hotpot{CLUSTER_NUM}')    
    clustered_embs, doc_emb_map = get_embs_by_cluster()
    # print doc_emb_map dimension per cluster
    # for i in range(CLUSTER_NUM):
    #     print(f"Cluster {i} has {len(doc_emb_map[i])} embeddings")
    # write_cluster_embs(clustered_embs,f'cluster/hotpot{CLUSTER_NUM}')
    write_doc_emb_map(doc_emb_map,f'cluster/hotpot{CLUSTER_NUM}')
    # copy_doc_list(f'cluster/hotpot{CLUSTER_NUM}')
    # sanity_check(doc_emb_map, (f'cluster/hotpot{CLUSTER_NUM}/doc_list.pkl'))
    # copy_question_json()
    
