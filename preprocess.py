import os
import argparse
from dotenv import load_dotenv
from src.mschema import MschemaCreator
from src.questioner import Questioner

load_dotenv()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset", type=str, choices=["spider", "bird"], default="spider")

    args = parser.parse_args()

    # create mschema
    ms = MschemaCreator(dataset=args.dataset)

    # generate prompts
    q = Questioner(dataset=args.dataset)

    print("Preprocessing done.")