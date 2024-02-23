import requests
from dotenv import load_dotenv
import os



#TODO: These values are limited to 10 labels each. As we have 113 labels, lets divide them into categories and query them in batches. If a label is < THRESHOLD, ignore them

class Engine():
    def __init__(self):
       self.__API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
       print(os.getenv("HF_SECRET"))
       self.__headers = {"Authorization": f"Bearer {os.getenv('HF_SECRET')}"}
       self.__labels = ['betrayal',
                  'competition',
                  'bank heist',
                  'neorealism',
                  'no background score',
                  'satire',
                  'robot',
                  'based on comic',
                  'sword and sandal',
                  'biker'
                  ]
   
    def query(self, prompt):
        payload = {
            "inputs": prompt,
            "parameters": {"candidate_labels" : self.__labels}
        }
        response = requests.post(self.__API_URL, headers=self.__headers, json=payload)
        print(response.json())
        return response.json()



