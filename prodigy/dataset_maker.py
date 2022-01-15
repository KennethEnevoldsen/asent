from datasets import load_dataset
import ndjson

dataset = load_dataset("DDSC/angry-tweets")
ds = dataset["train"]

data = list(ds)
data[0]
with open("angrytweets.jsonl", "w") as f:
    text = ndjson.dumps(list(ds))
    f.write(text)