# Usage Guide
1) [config.yaml](./config.yaml)의 default 형식을 override하여 Configuration을 작성한다
2) 저장한 config를 기반으로 `benchmark.Config` 클래스를 호출하여 `make_folder_tree` 메서드를 실행
3) `make_folder_tree` 메서드는 config.yaml에 따라 폴더트리와 README.md 파일을 만들어준다
4) `benchmark.~Reader` 클래스들로 Benchmark들을 깃헙, 허깅페이스에 읽어온다음 `~Reader.save` 메서드로 샘플을 저장해준다
