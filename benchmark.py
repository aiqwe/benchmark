import json
from functools import lru_cache
from datasets import load_dataset
import os
import random
from yaml import load_all, CLoader as Loader
from loguru import logger
from pygments import highlight, lexers, formatters
from typing import Union


def show(obj, colored: bool = True):
    """indent 넣어서 이쁘게 프린트해주기"""
    encoded = json.dumps(obj, indent=4, ensure_ascii=False)
    if colored:
        encoded = highlight(
            encoded,
            lexer=lexers.JsonLexer(),
            formatter=formatters.Terminal256Formatter(style="one-dark"),
        )
    print(encoded)


class Benchmark:
    def __init__(
        self,
        benchmark_name: str,
        path: str = None,
        name: str = None,
        num_proc: int = 6,
        dataset=None,
        dataset_option: dict = None,
    ):
        """
        Benchmark를 EDA하는 클래스

        Args:
            path: dataset의 path(hf)
            name: config로 전달되는 path값, ARC-Challenge, ARC-easy, logiqa-en ... 등
            num_proc: 작업 프로세스 수
        """
        hf_conf = HFDatasets()
        self.benchmark_name = benchmark_name
        self.path = path
        self.name = name
        self.dataset_option = dataset_option or {}
        if not path:
            self.path = hf_conf.config[benchmark_name]["path"]
        if not name:
            self.name = hf_conf.config[benchmark_name]["name"]
        if not isinstance(self.path, str) and not isinstance(self.name, str):
            raise ValueError("path and name must be strings")
        if not self.name:
            self.datasetdict = load_dataset(
                self.path, num_proc=num_proc, **self.dataset_option
            )
        else:
            self.datasetdict = load_dataset(
                self.path, self.name, num_proc=num_proc, **self.dataset_option
            )
        if not dataset:
            self.split = list(self.datasetdict.keys())
            self.prior_split = "train" if "train" in self.split else self.split[0]
            self.dataset = self.datasetdict[self.prior_split]
        else:
            self.dataset = dataset
        repr = f"\npath: {self.path}\n"
        repr += f"name: {self.name}\n"
        repr += f"total_split: {self.split}\n"
        repr += f"prior_split: {self.prior_split}\n"
        for s in self.split:
            repr += f"{s}: {len(self.datasetdict[s])}\n"
        self.repr = repr
        logger.info(self.repr)

    def show(
        self,
        split: str = None,
        sample: dict = None,
        category: str = None,
        idx: int = None,
        colored=True,
    ):
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
            samples = self.sample(dataset=dataset, category=category)

        if not idx:
            idx = random.randint(0, len(samples) - 1)
        show(samples[idx], colored=colored)

    def save(
        self,
        split: str = None,
        samples: list = None,
        path: str = None,
        category: str = None,
    ):
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
            samples = self.sample(dataset=dataset, category=category)
        if not path:
            file_name = f"{self.path.split('/')[-1] + '-' + self.name if self.name else self.path.split('/')[-1]}"
            path = f"./tasks/{self.benchmark_name}/{file_name}.json"
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            logger.info(f"{path}에 저장합니다.")
            logger.info(f"{len(samples)}의 샘플이 저장됩니다.")
            json.dump(samples, f, ensure_ascii=False, indent=4)

    def __repr__(self):
        return f"{self.repr}"

    @lru_cache
    def sample(self, split: str = None, dataset=None, category: str = None):
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
                sample = dataset.filter(
                    lambda x: x[category] == task, writer_batch_size=1000
                )
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
                    dic.update({k: dataset[random.randint(0, len(dataset) - 1)][k]})
                samples.append(dic)
        logger.info(f"총 {len(samples)}개의 샘플이 있습니다.")
        self.samples = samples
        return self.samples


class HFDatasets:
    def __init__(self, path: str = "hfdatasets.yaml"):
        with open(path, "r") as f:
            file = f.read()
            conf = list(load_all(file, Loader=Loader))[0]
        self.config = {k: v for k, v in conf.items() if not k.startswith("default")}
        for k, v in self.config.items():
            setattr(self, k, v)

    def get_all_names(self):
        """yaml내 벤치마크들의 전체 이름 출력"""
        return list(self.config.keys())

    def get_all_values(self, key: str):
        """벤치마크들의 key로 전달된 값의 value들만 출력"""
        return {
            k: v_v
            for k, v in self.config.items()
            for v_k, v_v in v.items()
            if v_k == key
        }

    def get_benchmark(self, name: str):
        """벤치마크의 전체 정보 출력"""
        return self.config[name]

    def make_folder_tree(self, key: Union[list, str] = None, overwrite: bool = False):
        # if key is none, make all benchmark folder tree
        if not key:
            key = self.get_all_names()

        if isinstance(key, str):
            key = [key]
        # Guide Markdown within the folder
        for k in key:
            # Make Folder Tree and README.md
            os.makedirs(f"tasks/{k}", exist_ok=True)
            guide_doc = f"tasks/{k}/README.md"
            if not overwrite and os.path.exists(f"tasks/{k}/README.md"):
                continue

            # Make default Markdown
            guide_doc_md = f"## {k}\n"
            for key, value in self.config[k].items():
                if value:
                    if isinstance(value, str) and key not in (
                        "url",
                        "paper",
                        "annotation",
                    ):
                        guide_doc_md += f"{key}: {value}  \n"
                    if isinstance(value, list):
                        guide_doc_md += f"{key}:  \n"
                        for value_ele in value:
                            guide_doc_md += f"    - {value_ele}  \n"
                    if key in ("url", "paper", "annotation"):
                        guide_doc_md += f"{key}: [{value}]({value})  \n"

            with open(f"tasks/{k}/README.md", "w") as f:
                f.write(guide_doc_md)
                logger.info(f"{guide_doc}을 초기화합니다")

    def __repr__(self):
        return f"HFDatasets:\n{self.get_all_names()}\nMore Details in self.config"
