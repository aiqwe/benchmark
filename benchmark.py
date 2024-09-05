import json
from functools import lru_cache
from datasets.utils.logging import set_verbosity_error
from datasets import Dataset
from datasets import load_dataset
import random
from loguru import logger

class Benchmark:

    def __init__(self, name: str, path: str = None, num_proc: int = 6):
        """
        Benchmark를 EDA하는 클래스

        Args:
            name: dataset의 path(hf)
            path: config로 전달되는 path값, ARC-Challenge, ARC-easy, logiqa-en ... 등
            num_proc: 작업 프로세스 수
        """
        self.name = name.split('/')[-1]
        self.path = path
        if not path:
            self.datasetdict = load_dataset(name, num_proc=num_proc)
        else:
            self.datasetdict = load_dataset(name, path, num_proc=num_proc)
        self.split = list(self.datasetdict.keys())
        self.prior_split = "train" if "train" in self.split else self.split[0]
        self.dataset = self.datasetdict[self.prior_split]
        repr = f"\nname: {name}\n"
        repr += f"path: {path}\n"
        repr += f"total_split: {self.split}\n"
        repr += f"prior_split: {self.prior_split}\n"
        for s in self.split:
            repr += f"{s}: {len(self.datasetdict[s])}\n"
        self.repr = repr
        logger.info(self.repr)

    def show(self, split: str = None, sample: dict = None, category: str = None, idx: int = None):
        """
        Sample 1개를 JSON indent = 4로 보여줌
        Args:
            split: 'train', 'test', 'validation'...
            sample: 보려는 샘플
            category: task를 나누는 카테고리, pass되면 카테고리마다 샘플링하는 list samples에서 sample로 뽑음
            idx: 보려는 samples의 index
        """
        if not split:
            dataset = self.dataset
        else:
            dataset = self.datasetdict[split]

        if not sample:
            samples = self.sample(dataset=dataset, category = category)

        if not idx:
            idx = random.randint(0, len(samples) - 1)
        print(json.dumps(samples[idx], indent=4, ensure_ascii=False))

    def save(self, split: str = None, samples: list = None, path: str = None, category: str = None):
        """
        samples를 저장함
        Args:
            split: 'train', 'test', 'validation'...
            samples: 저장하려는 samples
            path: 저장 path
        """

        if not split:
            dataset = self.dataset
        else:
            dataset = self.datasetdict[split]

        if not samples:
            samples = self.sample(dataset=dataset, category = category)
        if not path:
            path = f"./samples/{self.name + '-' + self.path if self.path else self.name.split('/')[-1]}.json"
        with open(path, "w") as f:
            logger.info(f"{path}에 저장합니다.")
            logger.info(f"{len(samples)}의 샘플이 저장됩니다.")
            json.dump(samples, f, ensure_ascii = False, indent = 4)

    @lru_cache
    def sample(self, split: str = None, dataset = None, category: str = None):
        """
        dataset에서 sampling하기, 카테고리가 있으면 카테고리마다 1개씩 샘플링함
        Args:
            dataset: 샘플링할 데이터셋
            category: 구분하려는 카테고리
        """

        if not split:
            dataset = self.dataset
        else:
            dataset = self.datasetdict[split]

        if category is not None:
            logger.info("카테고리가 있어서 카테고리마다 3개씩 샘플링합니다")
            samples = []

            for task in dataset.unique(category):
                sample = dataset.filter(lambda x: x[category] == task, writer_batch_size = 1000)
                iteration = 3
                for idx in range(iteration):
                    dic = {}
                    for k in sample.features.keys():
                        dic.update({k: sample[random.randint(0, len(sample) - 1)][k]})
                    samples.append(dic)
        if category is None:
            logger.info("카테고리가 없어서 전체에서 20개를 샘플링합니다")
            samples = []
            iteration = 20

            for idx in range(iteration):
                dic = {}
                for k in dataset.features.keys():
                    dic.update({k: dataset[random.randint(0, len(dataset)-1)][k]})
                samples.append(dic)
        logger.info(f"총 {len(samples)}개의 샘플이 있습니다.")
        self.samples = samples
        return self.samples

