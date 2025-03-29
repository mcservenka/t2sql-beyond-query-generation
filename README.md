# Beyond Query Generation

State-of-the-Art Text-to-SQL benchmarks represent one-dimensional challenges for modern LLMs, assuming answerability for every question in a dataset. However, in practical applications unanswerable user inputs have to be handles accordingly as well. This repository provides the source code for the paper **Beyond Query Generation: Assessing Unanswerable Questions in Text-to-SQL**, which addresses this gap by augmenting the Spider and BIRD-SQL datasets and evaluating four modern LLMs on their ability to identify unanswerable questions. In order to reproduce the results, follow the instructions below.

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
Additionally, you need to copy [BIRD-SQL's](https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/bird) `evaluation.py` from `DAMO-ConvAI/bird/llm/src` to `./external/bird`.  <br>
Make sure to define the OpenAI and TogetherAI keys in your environment variables as `OPENAI_API_KEY`, `OPENAI_API_ORGANIZATION`, `OPENAI_API_PROJECT` and `TOGETHERAI_API_KEY`. You can also use the `dotenv`-package.

## Environment Setup
Now set up the Python environment:
```submodules
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
## Experiment
Follow the steps down below to recreate the experiment.
### Preprocessing
To execute the preprocessing procedures run `preprocess.py` and set the dataset parameter to 'spider' or 'bird'. This will create the M-Schemas and final prompts.
```
python preprocess.py --dataset spider
```

### Generate Predictions
In terms of LLMs utilized within this study, open- and closed-source LLMs were tested, which is common in this field of research. The first category consists of the models `Qwen/Qwen2.5-Coder-32B-Instruct` and `meta-llama/Llama-3.3-70B-Instruct-Turbo` provided by TogetherAI (`together`). For close-source models `gpt-4o-2024-08-06` and `gpt-3.5-turbo-0125` by OpenAI (`openai`) were selected. To generate the individual results run the following command for each model and dataset:
```
python generate.py --dataset spider --provider openai --model gpt-4o-2024-08-06
```

### Evaluate Results
To evaluate the results run the following:
```
python evaluate.py --dataset spider --model gpt-4o-2024-08-06
```

## Results
Please note that the results may vary due to the inherent stochasticity of the LLM. For detailed evaluation results feel free to check out chapter 5 of the paper. 
<table>
    <tr>
        <td> TDExA by Model </td>
        <td> Spider </td>
        <td> BIRD-SQL </td>
    </tr>
    <tr>
        <td> GPT-4o </td>
        <td> 78.67 % </td>
        <td> 58.85 % </td>
    </tr>
    <tr>
        <td> GPT-3.5-turbo </td>
        <td> 66.39 % </td>
        <td> 48.99 % </td>
    </tr>
    <tr>
        <td> Qwen-2.5 </td>
        <td> 82.70 % </td>
        <td> 55.73 % </td>
    </tr>
    <tr>
        <td> Llama-3.3 </td>
        <td> 77.59 % </td>
        <td> 58.91 % </td>
    </tr>
</table>

## Citation
```citation
@article{beyond-query-generation,
    author  =   {Cservenka Markus},
    title   =   {Beyond Query Generation: Assessing Unanswerable Questions in Text-to-SQL},
    year    =   {2025}
}
```


    
