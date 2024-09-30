# lambada
- 전체 문단을 봤을 때는 마지막 단어를 예측할 수 있지만, 오직 이전 문장만 봤을 땐 마지막 단어를 예측하기 어렵다는 것에 기반함
    - 아래와 같이 각 문장만 보면 말이 되지만, 전체적인 맥락에선 오락가락 하는 모습임
    
    ```json
    {
        "Human": "What is your job?",
        "Machine": "I'm a lawyer.",
        "Human": "What do you do?",
        "Machine": "I'm a doctor."
    }
    ```
    
- LAMBADA는 Context와 Target Sentence로 구성되며, Target Sentence의 마지막 단어를 맞추는 Task임
- Bookcorpus에 기반한 데이터셋 사용
    - bookcorpus의 소설 데이터를 많이 이용함
---
+ **source**: huggingface
+ **hf_path**: EleutherAI/lambada_openai
+ **url**: [https://huggingface.co/datasets/EleutherAI/lambada_openai](https://huggingface.co/datasets/EleutherAI/lambada_openai)  
+ **paper**: [https://arxiv.org/pdf/1606.06031](https://arxiv.org/pdf/1606.06031)  
