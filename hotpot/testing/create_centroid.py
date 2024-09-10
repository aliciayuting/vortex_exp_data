import numpy as np
import pickle
# Create a 2D numpy array with shape (1, 1024)
testcentroid = np.zeros((1, 1024))

# Save the data as a pickle file
with open('centroids.pkl', 'wb') as file:
    pickle.dump(testcentroid, file)