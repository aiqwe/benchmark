# mmlu_pro
- GPT4, Gemini, Claude등 SOTA LLM들이 MMLU 포화상태임
- MMLU는 프롬프트와 Scoring Function 들에 민감함
    - 프롬프트에 따라 Accuracy가 많이 바뀌기도 함
- MMLU는 Knowledge 기반이라 Reasoning 평가가 떨어짐
- 기존 MMLU에서 선택지를 4개 → 10개로 늘림
- 대학 수준의 Exam 문제들을 늘림, 모델이 Reasoning을하도록 유도함
- 총 14개의 주제
- 12032개의 문제셋
- 기존 MMLU, STEM Website, TheoremQA, Scibench 등에서 데이터를 수집
---
+ **source**: huggingface
+ **hf_path**: TIGER-Lab/MMLU-Pro
+ **url**: [https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro)  
+ **paper**: [https://arxiv.org/pdf/2406.01574](https://arxiv.org/pdf/2406.01574)  
