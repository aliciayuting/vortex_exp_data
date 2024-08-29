import json
import numpy as np
import pickle

import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string.
    text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002 use the cl100k_base
    more detailed notes: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb 
    max input size is 8191 for all three
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens



def get_docs(data_path):
     docs = []
     doc_id = 0
     total_tokens = 0
     with open(data_path, 'r') as f:
          data = json.load(f)
          for d in data:
               for context in d['context']:
                    title = context[0]
                    sentences = context[1]
                    paragraphs = " ".join(sentences)
                    num_tokens = num_tokens_from_string(paragraphs, "cl100k_base")
                    if (num_tokens > 8191):
                         print(f"Doc {doc_id} has more than 8191 tokens")
                    else:
                         docs.append(paragraphs)
                         total_tokens += num_tokens
     print(f"Total number of documents: {len(docs)}, total tokens: {total_tokens}")
     np_docs = np.array(docs)
     return np_docs

def get_questions(data_path):
     questions = []
     with open(data_path, 'r') as f:
          data = json.load(f)
          for d in data:
               question = d['question']
               questions.append(question)
     print(f"Total number of questions {len(questions)}")
     return questions


def save_pkl(save_path, np_docs):
     with open(save_path, 'wb') as f:
          pickle.dump(np_docs, f)
     print(f"Content has been written to {save_path}")


# Base request structure
def create_request(document_text, custom_id):
    return {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/embeddings",  # Assuming you're using the embeddings endpoint
        "body": {
            "model": "text-embedding-3-small",  # Use your desired model
            "input": document_text
        }
    }

def create_batch_jsonl(jsonl_file_path, documents):
     print(len(documents))
     with open(jsonl_file_path, 'w') as jsonl_file:
          for i, doc in enumerate(documents):
               request = create_request(doc, custom_id=f"{i}")
               jsonl_file.write(json.dumps(request) + '\n')


def get_stored_documents(document_path):
     # read the documents in pickle
     with open(document_path, 'rb') as f:
          np_documents = pickle.load(f)
     return np_documents




if __name__ == "__main__":

     # 0. Get context doc
     # hotpot_train_data_path = 'hotpot_train_v1.1.json'
     # docs_file_name = "hotpot_context.pkl"     
     # np_docs = get_docs(hotpot_train_data_path)
     # print(np_docs.shape)
     # save_pkl(docs_file_name, np_docs)
     
     # 1. Output context to jsonl
     # np_documents = get_stored_documents(docs_file_name)
     # # create_batch_jsonl(jsonl_file_name, np_documents.tolist())
     # jsonl_file_name = 'hotpot_train_v1.1_context.jsonl'
     # create_batch_jsonl(jsonl_file_name, np_documents.tolist())
     # print(f"Jsonl file has been written to {jsonl_file_name}, with toal of {len(np_documents)} documents")
     
     # 2. Get questions
     hotpot_train_data_path = 'hotpot_train_v1.1.json'
     questions_file_name = "hotpot_questions.pkl"
     questions = get_questions(hotpot_train_data_path)
     save_pkl(questions_file_name, questions)
     

