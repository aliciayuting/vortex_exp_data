import openai
import numpy as np
import pickle
import argparse



with open('hotpot_context.pkl', 'rb') as f:
     documents = pickle.load(f)


def get_embeddings(client, documents, model="text-embedding-3-large"):
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


def get_batch_embeddings(client,documents, batch_size=20, model="text-embedding-3-large"):
     all_embeddings = []
     for i in range(0, len(documents), batch_size):
          batch = documents[i:i + batch_size]
          batch_embeddings = get_embeddings(client,batch, model=model)
          all_embeddings.append(batch_embeddings)
     return np.vstack(all_embeddings)


def save_embeddings(save_pathname, embeddings):
     with open(save_pathname, 'wb') as f:
          pickle.dump(embeddings, f)
     print(f"Embeddings have been written to {save_pathname}")


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
     embeddings = get_embeddings(client, documents)
     print(embeddings.shape)
     # embeddings = get_batch_embeddings(client,documents, batch_size=20)
     # print(embeddings)

     save_embeddings("hotpot_embeddings.pkl", embeddings)

