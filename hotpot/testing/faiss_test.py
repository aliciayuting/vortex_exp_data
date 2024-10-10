import faiss
import numpy as np
import pickle

# Assuming emb_list is a list of embeddings and question_doc is the query vector

QUESTION_TO_SEARCH = 0

def load_pickle(file_path):
    data = None
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data


folder = './dataset/'
emb_list = load_pickle(f'{folder}embeddings_list.pkl')
docs = load_pickle(f'{folder}doc_list.pkl')
questions = load_pickle(f'{folder}questions.pkl')
question_embeddings = data = np.loadtxt(f'{folder}query_emb.csv', delimiter=',')
#question_embeddings = load_pickle(f'{folder}questions_embeddings.pkl')


print(len(emb_list))
emb_list = np.array(emb_list).astype('float32')  # Ensure the embeddings are in float32
question_doc = np.array(question_embeddings[QUESTION_TO_SEARCH]).astype('float32')  # Ensure the query is in float32

# Get the dimension of the embeddings
dimension = emb_list.shape[1]  # Assumes emb_list is a 2D array (num_embeddings, embedding_dim)
print(dimension)
# Create a FAISS index, here we're using an IndexFlatL2 which is a basic index with L2 distance
index = faiss.IndexFlatL2(dimension)

# Add embeddings to the index
index.add(emb_list)

# Search for the nearest 5 neighbors
k = 5  # number of nearest neighbors
distances, indices = index.search(question_doc.reshape(1, -1), k)

# Print the results
print("Indices of nearest neighbors:", indices)
print("Distances to nearest neighbors:", distances)

print("\nQuestion:", questions[QUESTION_TO_SEARCH],"\n")
for i, index in enumerate(indices[0]):
    #print(f"Question: {questions[index]}")
    print(f"Context: {docs[index]}")
    print(f"Distance: {distances[0][i]}")
