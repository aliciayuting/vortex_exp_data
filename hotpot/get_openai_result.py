import openai
import argparse
import json
import pickle
import numpy as np

if __name__ == "__main__":
     parser = argparse.ArgumentParser(description="Process OpenAI API Key")
     parser.add_argument(
          "--openai_key",
          type=str,
          required=True,
          help="Your OpenAI API key"
     )
     parser.add_argument(
          "--batch_job_id",
          type=str,
          required=True,
          help="Your OpenAI batch job id"
     )
     args = parser.parse_args()
     client = openai.Client(api_key=args.openai_key)
     
     batch_job = client.batches.retrieve(args.batch_job_id)



     print(f"batch job {args.batch_job_id}, status {batch_job.status} " )
     if batch_job.status == "completed":
          result_file_id = batch_job.output_file_id
          result = client.files.content(result_file_id).content
          result_file_name = 'result_hotpot_train_v1.1_context.jsonl'
          with open(result_file_name, 'wb') as file:
               file.write(result)
          print(f"Result has been written to {result_file_name}")
          
          results = {}
          # process result line by line
          with open(result_file_name, 'r') as file:
               for line in file:
                    res = json.loads(line)
                    request_id = int(res["custom_id"][8:])
                    embeddings = res["response"]["body"]["data"]
                    embedding = embeddings[0]["embedding"]
                    results[request_id] = embedding
                    if len(embeddings) != 1:
                         print(f"Error in embedding {request_id}, len {len(embeddings)}")
          # process results in order by the key to put them to a list
          res_embeddings = []
          for i in range(len(results)):
               if i not in results:
                    print(f"Error in embedding {i}")
               else:
                    res_embeddings.append(results[i])
          # write res_embeddings to pickle
          with open("embs/hotpot_train_v1.1_embeddings_top10.pkl", 'wb') as f:
               pickle.dump(np.array(res_embeddings), f)
     