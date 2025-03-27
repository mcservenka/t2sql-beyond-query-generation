# Beyond Query Generation

State-of-the-Art Text-to-SQL benchmarks represent one-dimensional challenges for modern LLMs, assuming answerability for every question in a dataset. However, in practical applications unanswerable user inputs have to be handles accordingly as well. This repository provides the source code for the paper **Beyond Query Generation: Assessing Unanswerable Questions in Text-to-SQL**, which addresses this gap by augmenting the Spider and BIRD-SQL datasets and evaluating four modern LLMs on their ability to identify unanswerable questions.

>Cservenka, Markus. "Beyond Query Generation: Assessing Unanswerable Questions in Text-to-SQL", 2025.

Link to paper following soon...

## Ressources
To set up the environment, start by downloading the development sets of [Spider](https://yale-lily.github.io/spider) and [BIRD-SQL](https://bird-bench.github.io/) to the folders `./data/datasets/spider` and `./data/datasets/bird/dev` respectively. The samples, which were created and defined in the scope of the paper, are located in `./data/no_answer`.
Then add the git submodules of [M-Schema](https://github.com/XGenerationLab/M-Schema) and [Test-Suite-Evaluation](https://github.com/taoyds/test-suite-sql-eval) to  `./external`:
```submodules
git submodule add https://github.com/XGenerationLab/M-Schema.git external/mschema
git submodule add https://github.com/taoyds/test-suite-sql-eval.git external/testsuitesqleval
git submodule update --init --recursive
```
Additionally, you need to copy [BIRD-SQL's](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/bird) evaluation.py from `DAMO-ConvAI/bird/llm/src` to `./external/bird`.

## Environment Setup
Now set up the Python environment:
```submodules
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
