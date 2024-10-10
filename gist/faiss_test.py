import numpy as np
import faiss

def fvecs_read(filename, dtype=np.float32, c_contiguous=True):
    fv = np.fromfile(filename, dtype=dtype)
    if fv.size == 0:
        return np.zeros((0, 0))
    dim = fv.view(np.int32)[0]
    assert dim > 0
    fv = fv.reshape(-1, 1 + dim)
    if not all(fv.view(np.int32)[:, 0] == dim):
        raise IOError("Non-uniform vector sizes in " + filename)
    fv = fv[:, 1:]
    if c_contiguous:
        fv = fv.copy()
    return fv

base = fvecs_read('../gist/gist_base.fvecs')
print("Base shape", base.shape)
#print(base[0])


groundtruth = fvecs_read('../gist/gist_groundtruth.ivecs', np.int32)
print("groundtruth shape",groundtruth.shape)
#print(groundtruth[0])

query = fvecs_read('../gist/gist_query.fvecs')
print("query shape", query.shape)


dimension = base.shape[1]  # Assumes emb_list is a 2D array (num_embeddings, embedding_dim)
print("dimension", dimension)
# Create a FAISS index, here we're using an IndexFlatL2 which is a basic index with L2 distance
index = faiss.IndexFlatL2(dimension)

# Add embeddings to the index
index.add(base)

# Search for the nearest 5 neighbors
k = 5  # number of nearest neighbors
distances, indices = index.search(query[0].reshape(1, -1), k)

# Print the results
print("Indices of nearest neighbors:", indices)
print("Distances to nearest neighbors:", distances)
print("groundtruth", groundtruth[0])
