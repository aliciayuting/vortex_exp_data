# read the pickle file and check the embeddings dimension

import pickle

# with open('hotpot_train_v1.1_embeddings_327000.pkl', 'rb') as f:
#      emb = pickle.load(f)
#      print(emb.shape)
     
# with open('hotpot_embeddings.pkl', 'rb') as f:
#      emb = pickle.load(f)
#      print(emb.shape)
#      print(type(emb[0][0]))


with open('question_embs/hotpot_train_v1.1_questions_0.pkl', 'rb') as f:
     emb = pickle.load(f)
     print(emb.shape)