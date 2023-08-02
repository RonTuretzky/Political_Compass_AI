from transformers import pipeline
from evaluate import evaluator
import evaluate
from datasets import load_dataset
import subprocess
token = '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'
subprocess.run(["huggingface-cli", "login", "--token", token])
pipe = pipeline("text-classification", model="RonTuretzky/pcm_model", device=0)

dataset = load_dataset("csv", data_files={'test': ["_test.csv"]}, encoding='latin1')['test']
metric = evaluate.load("accuracy")
task_evaluator = evaluator("text-classification")
label2id = {
    "Libertarian Left": 0,
    "Libertarian Right": 1,
    "Authoritarian Left": 2,
    "Authoritarian Right": 3,
    "Centrist": 4,
    "Authoritarian Center": 5,
    "Left": 6,
    "Right": 7,
    "Libertarian Center": 8,
}
results = task_evaluator.compute(model_or_pipeline=pipe, data=dataset, metric=metric,
                                 label_mapping=label2id, )
print(results)