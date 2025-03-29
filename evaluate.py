import os
import argparse
from dotenv import load_dotenv
from src.evaluator import Evaluator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset", type=str, choices=["spider", "bird"], default="spider")
    parser.add_argument("--model", type=str, 
                        choices=["gpt-4o-2024-08-06", "gpt-3.5-turbo-0125", 
                                 "Qwen/Qwen2.5-Coder-32B-Instruct", "meta-llama/Llama-3.3-70B-Instruct-Turbo"], 
                        default="gpt-4o-2024-08-06")

    args = parser.parse_args()

    # evaluate results
    eval = Evaluator(dataset=args.dataset, model=args.model)
    if args.dataset == "spider":
        eval.evaluate_spider()
    elif args.dataset == "bird":
        eval.evaluate_bird()

    print("-- TDEXA ----------------")
    eval.print_tdexa()
    print("-- CONFUSION MATRIX ----------------")
    eval.print_confusion_matrix()

    print("Evaluation done.")