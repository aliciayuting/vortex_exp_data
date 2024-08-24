import openai
import numpy as np
import pickle
import argparse




def get_embeddings(client, documents, model="text-embedding-3-small"):
     """
     input: could be string or a list of strings(any array must be less than 2048 dimensions)
     dimensions: default 1536 for text-embedding-3-small
                    3072 for text-embedding-3-large
     encoding_format: default float
     """
     if isinstance(documents, np.ndarray):
          documents = documents.tolist()
     response = client.embeddings.create(
          model=model,
          input=documents,
          dimensions=1024
     )
     embeddings = [res.embedding for res in response.data]
     return np.array(embeddings)


def save_embeddings(save_pathname, embeddings):
     with open(save_pathname, 'wb') as f:
          pickle.dump(embeddings, f)
     print(f"Embeddings have been written to {save_pathname}")


def get_store_batch_embeddings(client,documents, batch_size=100, model="text-embedding-3-small"):
     """
     This method only send docs in batch, but doesn't have price benefit; if want batch discount use 
     batch_file_upload method
     """
     all_embeddings = []
     process_embedding_count = 0
     print("total num of batch:", len(documents)//batch_size)
     for i in range(0, len(documents), batch_size):
          if i < 325000:
               continue
          batch = documents[i:i + batch_size]
          batch_embeddings = get_embeddings(client,batch, model=model)
          all_embeddings.append(batch_embeddings)
          if i % 10 == 0:
               embs = np.vstack(all_embeddings)
               intermediate_store_path = f"embs/hotpot_train_v1.1_embeddings_{i}.pkl"
               save_embeddings(intermediate_store_path, embs)
               all_embeddings = []
               print(f"Processed {i} batch, dim {embs.shape}")
          process_embedding_count += len(batch)
          
     # return np.vstack(all_embeddings)



def batch_file_upload(client, jsonl_file_path):
     batch_input_file = client.files.create(
          file=open(jsonl_file_path, "rb"),
          purpose="batch"
     )
     batch_input_file_id = batch_input_file.id

     # completion_window only support 24h
     batch_job = client.batches.create(
               input_file_id=batch_input_file_id,
               endpoint="/v1/embeddings",
               completion_window="24h",
               metadata={
                    "description": "Embedding requests for HotpotQA context"
               }
          )
     print(f"Batch job created with id: {batch_job.id}")


if __name__ == "__main__":
     parser = argparse.ArgumentParser(description="Process OpenAI API Key")
     parser.add_argument(
          "--openai_key",
          type=str,
          required=True,
          help="Your OpenAI API key"
     )
     args = parser.parse_args()
     client = openai.Client(api_key=args.openai_key)
     
     documents = []
     with open('hotpot_context.pkl', 'rb') as f:
          documents = pickle.load(f)
     print(f"Total number of documents: {len(documents)}")
     
     # method 1
     # embeddings = get_embeddings(client, documents)
     # print(embeddings.shape)
     
     # method 2
     get_store_batch_embeddings(client, documents, batch_size=1000, model="text-embedding-3-small")
     # print(embeddings.shape)

     # method 3, cheapest method
     # save_embeddings("hotpot_train_v1.1_embeddings.pkl", embeddings)
     # jsonl_file_name = 'hotpot_train_v1.1_context.jsonl'
     # batch_file_upload(client, jsonl_file_name)

