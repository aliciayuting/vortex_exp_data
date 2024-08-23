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
     with open(data_path, 'r') as f:
          data = json.load(f)
          for d in data:
               for context in d['context']:
                    title = context[0]
                    sentences = context[1]
                    paragraphs = " ".join(sentences)
                    print(num_tokens_from_string(paragraphs, "cl100k_base"))
                    docs.append(paragraphs)
                    break
               if len(docs) == 10:
                    break
     np_docs = np.array(docs)
     return np_docs

def save_docs(save_path, np_docs):
     with open(save_path, 'wb') as f:
          pickle.dump(np_docs, f)
     print(f"Doc context has been written to {save_path}")



if __name__ == "__main__":

     hotpot_train_data_path = 'hotpot_train_v1.1.json'
     save_file_name = "hotpot_context.pkl"
     
     np_docs = get_docs(hotpot_train_data_path)
     print(np_docs.shape)
     save_docs(save_file_name, np_docs)

     

