import json
from datasets.utils.logging import set_verbosity_error
from datasets import Dataset
import random

set_verbosity_error()

def show(sample: dict):
    print(json.dumps(sample, indent=4, ensure_ascii=False))
    
def save(sample: dict, path: str):
    with open(path, "w") as f:
        json.dump(sample, f, ensure_ascii = False, indent = 4)
        
def sample(dataset, category: str = None):
    
    if category is not None:
        samples = []
    
        for task in dataset.unique(category):
            sample = dataset.filter(lambda x: x[category] == task, writer_batch_size = 1000)[0]
            samples.append(sample)
    if category is None:
        samples = []
        dic = {}
        iteration = 20
        
        for idx in range(iteration):
            dic = {}
            for k in dataset.features.keys():
                dic.update({k: dataset[random.randint(0, len(dataset)-1)][k]})
            samples.append(dic)
       
    return samples

