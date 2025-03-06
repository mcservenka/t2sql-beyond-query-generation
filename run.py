import os
from dotenv import load_dotenv
from src.mschema import MschemaCreator
from src.questioner import Questioner
from src.llm import OpenAIAPI
from src.evaluator import Evaluator

load_dotenv()

# open source models on huggingface
#   - Llama 3 70B: https://huggingface.co/meta-llama/Meta-Llama-3-70B
#   - Deepseek R1: https://huggingface.co/deepseek-ai/DeepSeek-R1
#   - SQLCoder 34B: https://huggingface.co/defog/sqlcoder-34b-alpha



# create M Schema json and txt files
# ms_spider = MschemaCreator(dataset="spider")
# ms_bird = MschemaCreator(dataset="bird")

# generate prompts for llm
#q_spider = Questioner(dataset="spider")
#q_bird = Questioner(dataset="bird")

# ask llm
#gpt4o_spider = OpenAIAPI(dataset="spider", model="gpt-4o-2024-08-06")
#gpt35_spider = OpenAIAPI(dataset="spider", model="gpt-3.5-turbo-0125")
#gpt4o_bird = OpenAIAPI(dataset="bird", model="gpt-4o-2024-08-06")
#gpt4o_bird.generate_results(overwrite=False)
#gpt4o_bird.prep_evaluation()


#"meta-llama/Llama-3.3-70B-Instruct-Turbo"
#"Qwen/Qwen2.5-Coder-32B-Instruct"
#qwen_spider = OpenAIAPI(dataset="bird", provider="together", model="Qwen/Qwen2.5-Coder-32B-Instruct")
#qwen_spider.generate_results(overwrite=False)
#qwen_spider.prep_evaluation()

# evaluate results

eval = Evaluator(dataset="bird", model="Qwen/Qwen2.5-Coder-32B-Instruct")
eval.evaluate_bird()

