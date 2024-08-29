
import pickle
from hotpot_preprocess import *
import csv

# questions = get_questions('hotpot_train_v1.1.json')
NUM_TO_GET = 1500

# write it to query.csv
with open('query.csv', 'w') as f:
     for i, question in enumerate(questions):
          if i > NUM_TO_GET:
               break
          if i == NUM_TO_GET:
               f.write(f"{question}")
          else:
               f.write(f"{question}\n")

questions_embs = []
with open('question_embs/hotpot_train_v1.1_full_question_emb3small.pkl', 'rb') as f:
     questions_embs = pickle.load(f)
     print(questions_embs.shape)
     
np.savetxt('query_emb.csv', questions_embs[:NUM_TO_GET], delimiter=',', fmt='%f')

# with open('query_emb.csv', newline='') as csvfile:
#     csvreader = csv.reader(csvfile)

#     for row in csvreader:
#         num_elements = len(row)
        
#         print(f'Number of elements in this row: {num_elements}')
     


