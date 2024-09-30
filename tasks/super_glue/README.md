# super_glue
- GLUE의 난이도를 올린 버전
    - GLUE는 9가지 NLU Task를 포함하며, 공개된 데이터셋을 기반으로 작성된 벤치마크
    - Super GLUE는 GLUE의 디자인을 기반으로하며, 난이도 상승, Task 추가 버전(QA, Coreference Resolution)
- Super GLU는 다음 Task들을 포함함
    1. `BoolQ(Boolean Questions)` : QA Task. 위키피디아의 짧은 본문과 yes/no 질문으로 구성
    2. `CB(CommitmentBank)` : Entailment Task. WSJ나 소설 코퍼스로 구성
    3. `COPA(Choice of Plausible Alternatives)` : 인과관계를 추론하는 Task. 문장을 받고 원인 또는 결과로 결정해야함
    4. `MultiRC(Multi-Sentence Reading Comprehension)` : QA Task. 어떤 답변이 참이고 거짓인지 판단해야함
    5. `ReCoRD(Reading Comprehension with Commonsense Reasoning Dataset)` : 객관식 QA Task. 뉴스 기사에 마스킹된 개체를 예측해야함
    6. `RTE(Recognizing Textual Entailment)` : Text Entailment Task. 기존 GLUE에 포함되어 있음
    7. `WiC(Word-in-Context)` : 문장 Pair의 Binary Classification Task. 단어 의미가 중의적인지 판단해야함
    8. `WSC(Winograd Schema Challenge)` : Coreference Resolution Task. 선택지중 대명사의 올바른 참조 대상을 결정해야함
---
+ **source**: huggingface
+ **hf_path**: aps/super_glue
+ **hf_name**: 
    <details>
        <summary>Click</summary>
            <div>  -  <code>boolq</code></div>
            <div>  -  <code>cb</code></div>
            <div>  -  <code>copa</code></div>
            <div>  -  <code>multirc</code></div>
            <div>  -  <code>record</code></div>
            <div>  -  <code>rte</code></div>
            <div>  -  <code>wic</code></div>
            <div>  -  <code>wsc</code></div>
            <div>  -  <code>wsc.fixed</code></div>
            <div>  -  <code>axb</code></div>
            <div>  -  <code>axg</code></div>
    </details>
 
+ **url**: [https://huggingface.co/datasets/aps/super_glue](https://huggingface.co/datasets/aps/super_glue)  
+ **paper**: [https://arxiv.org/pdf/1905.00537](https://arxiv.org/pdf/1905.00537)  
