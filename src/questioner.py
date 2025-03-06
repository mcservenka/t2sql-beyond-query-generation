import os
import json

from configs.paths import MSCHEMAS_PATH, PROMPTS_PATH, SPIDER_DEV_PATH, SPIDER_NO_ANSWER_PATH, BIRD_DEV_PATH, BIRD_NO_ANSWER_PATH


class Questioner:

    def __init__(self, dataset:str = "spider"):
        
        self.dataset = dataset
        
        os.makedirs(PROMPTS_PATH, exist_ok=True)
        os.makedirs(f"{PROMPTS_PATH}{dataset}", exist_ok=True)

        if dataset == "spider":
            
            with open(SPIDER_DEV_PATH, "r") as f: 
                dev = json.load(f)
            with open(SPIDER_NO_ANSWER_PATH, "r") as f:
                noanswer = json.load(f)

        elif dataset == "bird":
            
            with open(BIRD_DEV_PATH, "r") as f: 
                dev = json.load(f)
            with open(BIRD_NO_ANSWER_PATH, "r") as f:
                noanswer = json.load(f)

        
        
        samples = dev + noanswer

        prompts = list()

        for sample in samples:
            db_id = sample["db_id"]
            query = sample.get("query", "0") if dataset == "spider" else sample.get("SQL", "0") # get query from spider or bird
            question = sample["question"]
            evidence = "" if dataset == "spider" else sample.get("evidence", "") # get evidence from spider or bird
            schema = self.get_schema_str(db_id)

            prompt = self.build_prompt(schema, question, evidence)

            prompts.append({
                "db_id": db_id,
                "question": question,
                "gold_query": query,
                "prompt": prompt
            })
        
        with open(f"{PROMPTS_PATH}{dataset}/prompts.json", "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=4)

        print(f"Prompts of {self.dataset} ready.")
    

    def build_prompt(self, schema, question, evidence):

        p_preamble = """You are now a sqlite data analyst, and you are given a database schema as follows:\n\n"""

        p_schema = f"{schema}\n\n"

        p_question = f"{question}\n\n"

        p_evidence = f"{evidence}\n\n"

        p_instruction = """Please read and understand the database schema carefully, and generate an executable SQL based on the user's question and evidence. The generated SQL is protected by ```sql and ```.\n"""

        p_note = """If you think that the user's question cannot be solved given the database schema, just answer with '0'."""

        return p_preamble + p_schema + p_question + p_evidence + p_instruction + p_note

        
    def get_schema_str(self, db_id: str = None):
        
        with open(f"{MSCHEMAS_PATH}{self.dataset}/{db_id}/{db_id}.txt", "r", encoding="utf-8") as file:
            schema = file.read()
        
        return schema
