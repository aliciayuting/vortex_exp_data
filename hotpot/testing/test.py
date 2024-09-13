import pickle
import numpy as np
import json

def hotpot_data_examples():
    with open('../hotpot_train_v1.1.json') as f:
        data = json.load(f)
    print(json.dumps(data[0], indent=2), "\n\n")
    #print(json.dumps(data[32], indent=2))
    print(json.dumps(data[1], indent=2), "\n\n")
    print(json.dumps(data[2], indent=2), "\n\n")
    print(json.dumps(data[3], indent=2), "\n\n")
    print(json.dumps(data[4], indent=2), "\n\n")
    
def query_embs_test():
    data = np.loadtxt('../hotpot10/query_emb.csv', delimiter=',')

    # Print the loaded 2D array
    print(len(data[0]))
    print(data.shape)

def cluster_doc_test():
    with open('../hotpot10/cluster_0.pkl', 'rb') as file:
    #with open('./jamalbaai10k/embeddings_list.pkl', 'rb') as file:
        data = pickle.load(file)
    # Print the loaded 2D array
    print(len(data))
    print(len(data[0]))
    #print(data.shape)

def centroids_test():
    data = None
    with open('../hotpot10/centroids.pkl', 'rb') as file:
    #with open('./jamalbaai10k/centroids.pkl', 'rb') as file:
        data = pickle.load(file)
    # Print the loaded 2D array
    print(len(data))
    print(len(data[0]))
    print(data.shape)
    print(data)

def doc_embs_test():
    data = None
    # Open the pickle file
    with open('./jamalbaai10k/doc_emb_map.pkl', 'rb') as file:
    #with open('../hotpot10/doc_emb_map.pkl', 'rb') as file:
    #with open('./jamalbaai10k/centroids.pkl', 'rb') as file:
        # Load the data from the pickle file
        data = pickle.load(file)

    # Print the first item
    #print(data[0])
    print(type(data))
    print(len(data))
    print(type(data[0]))
    print(len(data[0]))

def firstdocs():
    with open('../hotpot10/doc_list.pkl', 'rb') as file:
    #with open('./jamalbaai10k/doc_list.pkl', 'rb') as file:
        data = pickle.load(file)
    print(data[0])
    print(data[1])
    print(data[2])
    print(data[3])
    print(data[4])
    print(data[5])
    print(data[6])
    print(data[7])
    print(data[8])
    print(data[9])

def fixdocmap():
    doc_emb_map = {0:{}}
    docs = None
    with open('./jamalbaai10k/doc_list.pkl', 'rb') as file:
        docs = pickle.load(file)
    for i in range(len(docs)):
        doc_emb_map[0][i] = i
    with open(f'doc_emb_map.pkl', 'wb') as f:
        pickle.dump(doc_emb_map, f)
#hotpot_data_examples()
#fixdocmap()
#doc_embs_test()
#cluster_doc_test()
centroids_test()