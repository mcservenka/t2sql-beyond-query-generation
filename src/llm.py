import os
import json
from tqdm import tqdm
from openai import OpenAI

from src.utils import extract_sql
from configs.paths import RESULTS_PATH, PROMPTS_PATH

# openai api parameters
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_ORGANIZATION = os.getenv('OPENAI_API_ORGANIZATION')
OPENAI_API_PROJECT = os.getenv('OPENAI_API_PROJECT')

# together api parameters
TOGETHERAI_API_KEY = os.getenv('TOGETHERAI_API_KEY')


class OpenAIAPI:

    def __init__(self, dataset: str = "spider", provider:str = "openai", model:str = "gpt-4o-2024-08-06"):

        self.dataset = dataset
        self.model = model
        model_name = model.split("/")[-1]
        self.responses = list()
        self.error_idx = list()
        self.r_path = f"{RESULTS_PATH}{self.dataset}/{model_name}/"

        os.makedirs(RESULTS_PATH, exist_ok=True)
        os.makedirs(f"{RESULTS_PATH}{dataset}", exist_ok=True)

        with open(f"{PROMPTS_PATH}{self.dataset}/prompts.json", "r", encoding="utf-8") as f:
            prompts = json.load(f)
            self.prompts = prompts

        if provider == "openai":
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
                organization=OPENAI_API_ORGANIZATION,
                project=OPENAI_API_PROJECT,
            )
        elif provider == "together":
            self.client = OpenAI(
                api_key=TOGETHERAI_API_KEY,
                base_url="https://api.together.xyz/v1"
            )
        else:
            print("ATTENTION: Unknown provider.")


    def ask_llm(self, question: str):
         
        try:
            res = self.client.chat.completions.create(
                model=self.model,
                messages = [
                    {"role": "user",
                    "content": question}
                ],
                temperature=0,
                max_tokens=400,
                n=1
            )
            
            try:
                response = res.choices[0].message.content
            except:
                response = res

            return dict(
                response=response,
                completion_tokens=res.usage.completion_tokens,
                prompt_tokens=res.usage.prompt_tokens,
                model=res.model,
                error=False
            )
        except Exception as e:
            print(f"Failed to connect to OpenAI API: {e}")
            return dict(
                response=e,
                error=True
            )
        
    def generate_results(self, overwrite:bool = False):

        if os.path.exists(self.r_path) and not overwrite:
            print("Results already exist. If you want to overwrite: overwrite=True")
            return
        
        os.makedirs(self.r_path, exist_ok=True)

        # reset result files
        with open(self.r_path + "raw_responses.txt", "w", encoding="utf-8") as rf: pass
        with open(self.r_path + "gold.txt", "w", encoding="utf-8") as gf: pass        

        print("Starting with prompting LLM.")
        for i, prompt in tqdm(enumerate(self.prompts)):
            response = self.ask_llm(question=prompt["prompt"])
            
            if response["error"]: self.error_idx.append(i)

            response["gold"] = prompt["gold_query"]
            response["db_id"] = prompt["db_id"]

            # raw response output            
            with open(self.r_path + "raw_responses.txt", "a", encoding="utf-8") as rf:
                rf.write("###\n" + str(response) + "\n###\n\n")
            
            # gold txt file            
            with open(self.r_path + "gold.txt", "a", encoding="utf-8") as gf:
                gf.write(prompt["gold_query"] + "\t" + response["db_id"] + "\n")

            self.responses.append(response)

        with open(self.r_path + "responses.json", "w", encoding="utf-8") as jf:
            json.dump(self.responses, jf, ensure_ascii=False, indent=4)

        print("Responses generated!")

    def prep_evaluation(self):
        
        if self.dataset == "spider":

            with open(self.r_path + "responses.json", "r") as f:
                responses = json.load(f)
            with open(self.r_path + "pred.txt", "w") as pf: pass

            for response in responses:
                try:
                    prediction = extract_sql(response["response"])
                except:
                    prediction = "0"
                
                with open(self.r_path + "pred.txt", "a") as f: f.write(prediction + "\n")
        
        elif self.dataset == "bird":

            with open(self.r_path + "responses.json", "r") as f:
                responses = json.load(f)

            pred = dict()

            for i, response in enumerate(responses):
                try:
                    prediction = extract_sql(response["response"])
                except:
                    prediction = "0"
            
                pred[str(i)] = prediction + "\t----- bird -----\t" + response["db_id"]
            
            with open(self.r_path + "pred.json", "w", encoding="utf-8") as f:
                json.dump(pred, f, ensure_ascii=False, indent=4)


