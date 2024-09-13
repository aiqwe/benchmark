import json
from functools import lru_cache
from datasets import load_dataset
import os
import random
from yaml import load_all, CLoader as Loader
from loguru import logger
from pygments import highlight, lexers, formatters
from typing import Union
from template import README_TEMPLATE
from textwrap import dedent, indent
import requests


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


class HFReader:
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
        hf_conf = Config()
        self.benchmark_name = benchmark_name
        self.path = path
        self.name = name
        self.dataset_option = dataset_option or {}
        if not path:
            self.path = hf_conf.config[benchmark_name]["path"]
        if not name:
            self.name = hf_conf.config[benchmark_name]["name"]
        if not isinstance(self.name, str):
            if isinstance(self.name, list):
                self.name_list = hf_conf.config[benchmark_name]["name"]
                self.name = hf_conf.config[benchmark_name]["name"][
                    random.randint(0, len(self.name) - 1)
                ]
                logger.info(
                    f"name is type of list. randomly picked '{self.name}'\nall names are saved within 'self.name_list':\n{hf_conf.config[benchmark_name]['name']}"
                )
        if not isinstance(self.path, str):
            raise ValueError("path must be strings")
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
            self.prior_split = (
                "default" if "default" in self.split else self.split[0]
            )  # bigbench case
            self.dataset = self.datasetdict[self.prior_split]
        else:
            self.dataset = dataset
        repr = f"path: {self.path}\n"
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
            samples = self.sampling(dataset=dataset, category=category)

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
            samples = self.sampling(dataset=dataset, category=category)
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
    def sampling(self, split: str = None, dataset=None, category: str = None):
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


class Config:
    def __init__(self, path: str = "config.yaml"):
        with open(path, "r") as f:
            file = f.read()
            conf = list(load_all(file, Loader=Loader))[0]
        self.config = {k: v for k, v in conf.items() if not k.startswith("default")}
        for k, v in self.config.items():
            setattr(self, k, v)

    @property
    def all_names(self):
        return self.get_all_names()

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
            on_the_fly = {}
            for key, value in self.config[k].items():
                if isinstance(value, list):
                # toggle should be written in html tag like below:
                # <details>
                #    <summary> click </summary>
                #    <div>- <code>value</code></div>
                # </details>
                    lines = []
                    for idx, ele in enumerate(value):
                        if idx == 0:
                            indent_num= 8 # 첫번째 라인은 prefix = " "*4를 적용받으므로 8칸만 indent
                        else:
                            indent_num = 12 # 두번째 라인부터는 prefix를 적용받지 않으므로 12칸 indent
                        lines.append(indent(f"<div>  -  <code>{ele}</code></div>", prefix=" " * indent_num))
                    on_the_fly.update(
                                {key: indent(dedent(
                                """
                                    <details>
                                        <summary>Click</summary>
                                    {}
                                    </details>
                                """), prefix = " " * 4).format('\n'.join(lines))
                                })
                # path, name은 backtick 처리
                elif isinstance(value, str) and key in ("path", "name"):
                    on_the_fly.update({key: f"`{value}`"})
                else:
                    on_the_fly.update({key: value})
            # README_TEMPLATE:
            # {benchmark_name}
            # + ** source **: {source}
            # + ** hf_path **: {hf_path}
            # + ** hf_url **: {hf_url}
            # + ** url **: {url}
            # + ** name **: {name}
            # + ** hf_url **: [{hf_url}]({hf_url})
            # + ** paper **: [{paper}]({paper})
            # + ** annotation **: [{annotation}]({annotation})
            guide_doc_md = README_TEMPLATE.format(benchmark_name=k, **on_the_fly)
            # None이 있으면 해당 줄 삭제처리
            guide_doc_md_processed = []
            for line in guide_doc_md.split("\n"):
                if "None" in line:
                    continue
                else:
                    guide_doc_md_processed.append(line)
            guide_doc_md = "\n".join(guide_doc_md_processed)

            # 저장
            with open(f"tasks/{k}/README.md", "w") as f:
                f.write(guide_doc_md)
                logger.info(f"{guide_doc}을 초기화합니다")

    def __repr__(self):
        return "Benchmark List:\n{}---------- More details in self.config".format(
            "\n".join([f"  - {name}" for name in self.get_all_names()])
        )


class GithubReader:
    def __init__(self, user: str, repo: str, fpath: str = None):
        """
        Github 파일을 읽어옴

        Args:
            user: github user명, ex) 'aiqwe'
            repo: repo 이름 ex) 'papers', 'benchmark'
            fpath: 파일의 위치. ex) 'tasks/arc/ai2-arc-ARC-Challenge.json'
        """
        self.url = f"https://raw.githubusercontent.com/{user}/{repo}/master"
        self.user = user.lower()
        self.repo = repo.lower()
        self.fpath = fpath

    @lru_cache
    def get_jsonl(self, fpath: None):
        if not self.fpath:
            if not fpath:
                raise ValueError(
                    "if self.fpath is None, argument 'fpath' from 'get' should be passed"
                )
        else:
            if fpath:
                logger.info(f"{self.fpath} will be overwritten by {fpath}")
        self.fpath = fpath
        url = self.url + f"/{self.fpath}"
        response = requests.get(url)
        if self.fpath.endswith("jsonl"):
            self.data = [json.loads(obj) for obj in response.text.splitlines()]
        if self.fpath.endswith("json"):
            self.data = json.loads(response.text)
        return self.data

    def sampling(self, fpath=None, n: int = 1000):
        return self.get_jsonl(fpath)[:n]

    def show(self, fpath=None, idx=None, colored=True):
        samples = self.sampling(fpath)

        if not idx:
            idx = random.randint(0, len(samples) - 1)
        show(samples[idx], colored=colored)

    def save(self, fpath: str = None, path: str = None, n: int = 20):
        total = self.get_jsonl(fpath)
        samples = random.sample(total, k=n)
        if not path:
            file_name = self.repo + "-" + os.path.basename(self.fpath).split(".")[0]
            path = f"./tasks/{self.repo}/{file_name}.json"
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            logger.info(f"{path}에 저장합니다.")
            logger.info(f"{len(samples)}의 샘플이 저장됩니다.")
            json.dump(samples, f, ensure_ascii=False, indent=4)
