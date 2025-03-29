import os
import argparse
from dotenv import load_dotenv
from src.llm import OpenAIAPI

load_dotenv()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset", type=str, choices=["spider", "bird"], default="spider")
    parser.add_argument("--provider", type=str, choices=["openai", "together"], default="openai")
    parser.add_argument("--model", type=str, 
                        choices=["gpt-4o-2024-08-06", "gpt-3.5-turbo-0125", 
                                 "Qwen/Qwen2.5-Coder-32B-Instruct", "meta-llama/Llama-3.3-70B-Instruct-Turbo"], 
                        default="gpt-4o-2024-08-06")

    args = parser.parse_args()

    # generate results
    pred = OpenAIAPI(dataset=args.dataset, provider=args.provider, model=args.model)
    pred.generate_results(overwrite=False)

    print("Results generated.")
