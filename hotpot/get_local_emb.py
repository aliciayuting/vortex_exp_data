from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import time
import json
import tiktoken
import pickle
import os
import csv

HOTPOT_DATASET_LOC = '../hotpot_train_v1.1.json'
#EMBEDDINGS_LOC = './jamalbigscience10k/'
#MODEL_NAME = "bigscience/sgpt-bloom-7b1-msmarco"
EMBEDDINGS_LOC = './jamalbaai10k/'
MODEL_NAME = "BAAI/bge-large-en-v1.5"

NUM_DOCS = 1000
MAX_TOKENS = 2000

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string.
    text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002 use the cl100k_base
    more detailed notes: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb 
    max input size is 8191 for all three
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_question(hotpot_block):
    question = hotpot_block['question']
    return question

def get_docs(hotpot_block):
    docs = []
    doctitles = []
    #context = ['context']
    for context in hotpot_block['context']:
        title = context[0]
        doctitles.append(title)
        sentences = context[1]
        paragraphs = " ".join(sentences)
        #print(paragraphs)
        num_tokens = num_tokens_from_string(paragraphs, "cl100k_base")
        if (num_tokens > MAX_TOKENS):
            print(f"Doc has {num_tokens} tokens")
        else:
            #print(num_tokens)
            docs.append(paragraphs)
            #total_tokens += num_tokens
    return docs, doctitles

data = None
with open(HOTPOT_DATASET_LOC) as f:
    data = json.load(f)

docs = []
doctitles = []
questions = []
print("starting test")
#for i in range(len(data)):
range_len = NUM_DOCS
if NUM_DOCS == -1:
    range_len = len(data)
for i in range(range_len):
    block_docs, block_doc_titles = get_docs(data[i])
    docs.extend(block_docs)
    doctitles.extend(block_doc_titles)
    questions.append(get_question(data[i]))
print(len(docs))
print(len(questions))
print(len(doctitles))



# get rid of duplicate documents
duplicates = {}
for index, doc in enumerate(doctitles):
    if doc in duplicates:
        duplicates[doc].append(index)
    else:
        duplicates[doc] = [index]
duplicate_indexes = {doc: indexes for doc, indexes in duplicates.items() if len(indexes) > 0}
first_occurrence_indexes = {indexes[0] for indexes in duplicate_indexes.values()}
filtered_docs = [doc for i, doc in enumerate(docs) if i in first_occurrence_indexes]
filtered_titles = [doc for i, doc in enumerate(doctitles) if i in first_occurrence_indexes]

#for doc, indexes in duplicate_indexes.items():
    #print(f"Duplicate document: {doc}")
    #print(f"Indexes: {indexes}")

print(len(filtered_docs))
print(len(filtered_titles))
doctitles = filtered_titles
docs = filtered_docs
#print(docs[0])
#print(docs[1])
#print(json.dumps(data[0], indent=2))
#print(docs[789])
#print(docs[7211])
#exit(0)

# loads BAAI/bge-large-en-v1.5
embed_model = HuggingFaceEmbedding(model_name=MODEL_NAME)

#embed_model = HuggingFaceEmbedding(model_name="bigscience/sgpt-bloom-7b1-msmarco")


start_time = time.time()
embeddings_list = []

for i in range(len(docs)):
    embeddings = embed_model.get_text_embedding(docs[i])
    embeddings_list.append(embeddings)
    if i % 100 == 0:
        print(i)
    #print(len(embeddings))
    #print(embeddings)

questions_embeddings_list = []
for i in range(len(questions)):
    embeddings = embed_model.get_text_embedding(questions[i])
    questions_embeddings_list.append(embeddings)
    if i % 100 == 0:
        print(i)
    #print(len(embeddings))
    #print(embeddings)


end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time)
print(len(embeddings_list))
print(len(embeddings_list[0]))
print(len(docs))
# Save embeddings_list to a pickle file

doc_emb_map = {0:{}}
for i in range(len(docs)):
    doc_emb_map[0][i] = docs[i]

os.makedirs(EMBEDDINGS_LOC, exist_ok=True)

with open(f'{EMBEDDINGS_LOC}embeddings_list.pkl', 'wb') as f:
    pickle.dump(embeddings_list, f)

with open(f'{EMBEDDINGS_LOC}cluster_0.pkl', 'wb') as f:
    pickle.dump(embeddings_list, f)

with open(f'{EMBEDDINGS_LOC}doc_emb_map.pkl', 'wb') as f:
    pickle.dump(embeddings_list, f)

# Save docs to a pickle file
with open(f'{EMBEDDINGS_LOC}doc_list.pkl', 'wb') as f:
    pickle.dump(docs, f)

with open(f'{EMBEDDINGS_LOC}questions.pkl', 'wb') as f:
    pickle.dump(questions, f)

# with open(f'{EMBEDDINGS_LOC}query.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for item in questions:
#         writer.writerow([item])  # Write each item in a new row

NUM_TO_GET = len(questions)
with open(f'{EMBEDDINGS_LOC}query.csv', 'w') as f:
     for i, question in enumerate(questions):
          if i >= NUM_TO_GET:
               break
          if i == NUM_TO_GET-1:
               f.write(f"{question}")
          else:
               f.write(f"{question}\n")


with open(f'{EMBEDDINGS_LOC}questions_embeddings.pkl', 'wb') as f:
    pickle.dump(questions_embeddings_list, f)

# with open(f'{EMBEDDINGS_LOC}query_emb.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(questions_embeddings_list)  # Write all rows at once

np.savetxt('query_emb.csv', questions_embeddings_list, delimiter=',', fmt='%f')
