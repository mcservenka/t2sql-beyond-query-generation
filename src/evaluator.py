import json
import os
from tqdm import tqdm
from func_timeout import func_timeout

from external.testsuitesqleval.evaluation import Evaluator as TestSuiteEvaluator
from external.testsuitesqleval.process_sql import get_schema, Schema, get_sql
from external.testsuitesqleval.exec_eval import eval_exec_match

from external.bird.evaluation import execute_sql

from configs.paths import RESULTS_PATH, NO_ANSWER_PATH, BIRD_DEV_PATH


class Evaluator:

    def __init__(self, dataset: str = "spider", model:str = "gpt-4o-2024-08-06"):

        self.dataset = dataset
        self.model = model
        self.model_name = model.split("/")[-1]

        self.pred_path = f"{RESULTS_PATH}{dataset}/{self.model_name}/pred.txt"
        self.gold_path = f"{RESULTS_PATH}{dataset}/{self.model_name}/gold.txt"

        self.pred_list = load_sql_lines(self.pred_path)
        self.gold_list = load_sql_lines(self.gold_path)

        if dataset == "spider":
            self.db_path = f"data/datasets/{dataset}/database"
        elif dataset == "bird":
            self.db_path = f"data/datasets/{dataset}/dev/database"
            # in case of bird also load gold dev file for hardness score
            with open(BIRD_DEV_PATH, "r") as f:
                self.bird_dev = json.load(f)

        with open(f"{NO_ANSWER_PATH}{dataset}_no_answer.json", "r") as f:
            self.no_answer = json.load(f)

        print(f"Predictions Count: {len(self.pred_list)} | Gold Count: {len(self.gold_list)}")
        assert len(self.pred_list) == len(self.gold_list), "number of predictions and golds must equal"
    

    def evaluate_spider(self):
        
        Eval = TestSuiteEvaluator()
        scores = list()
        first_idx_no_answer = None # assumes no answer samples 

        for idx, pg in tqdm(enumerate(zip(self.pred_list, self.gold_list))):
            p, g = pg
            p_str = p[0]
            g_str, db = g
            db_name = db
            db = os.path.join(self.db_path, db, db + ".sqlite")
            schema = Schema(get_schema(db))

            if g_str == "0":

                exec_score = int(g_str == p_str) # check if p_str is 0
                if first_idx_no_answer is None: 
                    first_idx_no_answer = idx
                
                hardness = self.no_answer[idx - first_idx_no_answer]["level"]

            else:
                # print(g_str)
                g_sql = get_sql(schema, g_str)
                hardness = Eval.eval_hardness(g_sql)

                try: # in case p_str = 0, will give exec score of 0, which is what we want
                    p_sql = get_sql(schema, p_str)
                except:
                    # If p_sql is not valid, then we will use an empty sql to evaluate with the correct sql
                    p_sql = {
                    "except": None,
                    "from": {
                        "conds": [],
                        "table_units": []
                    },
                    "groupBy": [],
                    "having": [],
                    "intersect": None,
                    "limit": None,
                    "orderBy": [],
                    "select": [
                        False,
                        []
                    ],
                    "union": None,
                    "where": []
                    }
                
                exec_score = eval_exec_match(db=db, p_str=p_str, g_str=g_str, plug_value=False,
                                             keep_distinct=False, progress_bar_for_each_datapoint=False)
                
            scores.append({
                "pred": p_str,
                "gold": g_str,
                "hardness": hardness,
                "score": exec_score
            })
        
        with open(f"{RESULTS_PATH}{self.dataset}/{self.model_name}/eval_results.json", "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)
        
    def evaluate_bird(self):
        
        scores = list()
        first_idx_no_answer = None # assumes no answer samples 

        for idx, pg in tqdm(enumerate(zip(self.pred_list, self.gold_list))):
            p, g = pg
            p_str = p[0]
            g_str, db = g
            db_name = db
            db = os.path.join(self.db_path, db, db + ".sqlite")

            if g_str == "0":

                exec_score = int(g_str == p_str) # check if p_str is 0
                if first_idx_no_answer is None: 
                    first_idx_no_answer = idx
                
                hardness = self.no_answer[idx - first_idx_no_answer]["level"]
            
            else:

                try:
                    exec_score = func_timeout(30, execute_sql, args=(p_str, g_str, db))
                except:
                    exec_score = 0
                    
                hardness = self.bird_dev[idx]["difficulty"]

            scores.append({
                "pred": p_str,
                "gold": g_str,
                "hardness": hardness,
                "score": exec_score
            })
        
        with open(f"{RESULTS_PATH}{self.dataset}/{self.model_name}/eval_results.json", "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)


def load_sql_lines(path: str):
    with open(path) as f:
        qlist = []
        for l in f.readlines():
           qlist.append(l.strip().split('\t'))
    
    return qlist