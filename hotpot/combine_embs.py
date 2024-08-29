import os
import pickle
import numpy as np

# Directory containing the pickle files
directory = "question_embs/"

# List all files in the directory with a .pkl extension
pickle_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.pkl')]

# Initialize an empty list to store the loaded arrays
arrays = []

# Load each pickle file and append the array to the list
for file in pickle_files:
    with open(file, 'rb') as f:
        array = pickle.load(f)
        arrays.append(array)

# Optionally, combine the arrays into one array if needed
combined_array = np.concatenate(arrays, axis=0)
print(combined_array.shape)

# Save the combined array into a new pickle file
with open("hotpot_train_v1.1_full_question.pkl", 'wb') as f:
    pickle.dump(combined_array, f)

print("Combined array saved to combined_file.pkl")