# hellaswag
- SWAG를 베이스로 하는 NLI 벤치마크
    - HellaSWAG는 Input으로 문장이 들어오면, 다음에 발생할 상황을 고르는 문제
    - SWAG는 비디오 자막이 주어지면 다음에 발생할 상황 4가지중 하나를 고르는 벤치마크
- 데이터셋은 ActivityNet과 WikiHow를 사용
    - SWAG는 ActivityNet, LSMDC 데이터셋을 사용하지만 HellaSWAG는 ActivityNet만 사용
    - WikiHow를 통해 CommonSense Reasoning을 측정
- Adversarial Filtering(AF)를 통해 좀더 그럴듯한 오답지를 생성하여 벤치마크 난이도를 올림
---
+ **source**: huggingface
+ **hf_path**: Rowan/hellaswag
+ **url**: [https://huggingface.co/datasets/Rowan/hellaswag](https://huggingface.co/datasets/Rowan/hellaswag)  
+ **paper**: [https://arxiv.org/pdf/1905.07830](https://arxiv.org/pdf/1905.07830)  
