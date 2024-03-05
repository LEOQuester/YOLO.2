import requests
from dotenv import load_dotenv
import os
import re

class Engine():

    def __init__(self):
        self.__API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b-it"
        self.__headers = {"Authorization": f"Bearer {os.getenv('HF_SECRET')}"}

        self.__predefined_labels = [
            "americana", "shakespeare", "action hero", "alternate history", "ambiguous ending",
            "anti-hero", "bank heist", "battle", "betrayal", "biker", "blockbuster", "business",
            "coming of age", "competition", "conspiracy", "corruption", "criminal mastermind",
            "cyberpunk", "dark hero", "deus ex machina", "double cross", "dream sequence",
            "dystopia", "epic", "espionage", "experimental", "experimental film", "fairy tale",
            "famous line", "famous opening theme", "femme fatale", "fictional biography",
            "flashback", "heist", "hero", "high school", "investigation", "kidnapping", "knight",
            "kung fu", "medieval times", "monster", "neo noir", "neorealism", "ninja",
            "no background score", "nonlinear timeline", "on the run", "one against many",
            "one man army", "organized crime", "parenthood", "parody", "plot twist",
            "police corruption", "police detective", "post-apocalypse", "postmodern",
            "psychopath", "race against time", "redemption", "rescue", "road movie", "robbery",
            "robot", "romance", "satire","sadness", "self sacrifice", "serial killer", "shootout",
            "slasher", "spirituality", "steampunk", "superhero", "supernatural", "swashbuckler",
            "sword and sandal", "time travel", "vampire", "virtual reality", "wuxia", "zombie"
        ]

    def clean(self, output_text):

        print("HERE")

        #TODO: if error return error
        print(output_text)
        print(output_text[0])
        generated_text = output_text[0]['generated_text']
        print(generated_text)

        # Using regex to find labels within brackets
        labels_texts = re.findall(r'\[(.*?)\]', generated_text, re.IGNORECASE)


        valid_labels = []
        labels = []
        for labels_text in labels_texts:
            # Splitting the labels and cleaning up the text
            for label in labels_text.split(","):
                print(label)
                if label.lower().strip() in self.__predefined_labels:
                    labels.append(label.strip())

        return labels

    def query(self, prompt):
        payload = {
            'inputs': f"""
                  <start_of_turn>user
          Below is a prompt. classify the prompt into 3 or less of the following labels, Only return [label, label, label, label, label]:where labels are elements of {self.__predefined_labels} 
          Prompt: """ + prompt + """
          <end_of_turn>\n<start_of_turn>model
                """
        }
        print(payload)

        response = requests.post(self.__API_URL, headers=self.__headers, json=payload)
        json_response = response.json()
        print(json_response)
        labels = self.clean(json_response)
        print(labels)
        return labels
