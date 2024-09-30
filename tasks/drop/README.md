# drop
- Discrete Reasoning Over the content of Paragraphs
- 데이터소스는 Wikipedia에서 단락을 추출하고, 크라우드 소싱을 통해 단락을 베이스로 하여 QA Pair를 생성
- 다양한 카테고리를 포함하지만, 특히 스포츠 게임, 역사 구절들을 강조함
- 답변은 3가지 타입
    - `number` : 주로 스포츠 게임 요약 정보(스코어 등)
    - `date` : 역사적 구절에서 날짜
    - `span`: 단락의 텍스트 범위
---
+ **source**: huggingface
+ **hf_path**: ucinlp/drop
+ **url**: [https://huggingface.co/datasets/ucinlp/drop](https://huggingface.co/datasets/ucinlp/drop)  
+ **paper**: [https://arxiv.org/pdf/1903.00161](https://arxiv.org/pdf/1903.00161)  
