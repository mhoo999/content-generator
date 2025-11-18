# Content Generator

교육 콘텐츠 폴더 구조를 자동으로 생성하는 도구입니다.

## 기능

- 엑셀/CSV 파일에서 과정 데이터 파싱
- 자동으로 폴더 구조 생성
- subjects.json, data.json 자동 생성
- 템플릿 자동 선택 (2022 CT, 2023 IT)
- 데이터 검증

## 설치

```bash
# 의존성 설치
pip install -r requirements.txt

# 개발 모드로 설치
pip install -e .
```

## 사용법

### 기본 사용

```bash
# 엑셀 파일에서 생성
python -m content_generator --input 25ctvibec.xlsx --output /path/to/subjects

# CSV 파일 사용
python -m content_generator --input 25ctvibec.csv --output /path/to/subjects

# 템플릿 지정
python -m content_generator --input 25ctvibec.xlsx --template ct2022
```

### 옵션

- `--input, -i`: 입력 파일 (엑셀 또는 CSV)
- `--output, -o`: 출력 디렉토리 (기본: ./output)
- `--template, -t`: 템플릿 선택 (ct2022, it2023, auto)
- `--validate-only`: 검증만 수행
- `--dry-run`: 실제 생성 없이 미리보기
- `--verbose, -v`: 상세 로그 출력

## 엑셀/CSV 형식

필수 컬럼:
- 과정명
- 차시
- 차시번호
- 차시명
- 강의영상(mp4) 링크

선택 컬럼:
- 챕터구분
- 챕터명
- 다운로드(zip) 링크

## 프로젝트 구조

```
content-generator/
├── content_generator/
│   ├── __init__.py
│   ├── __main__.py       # CLI 진입점
│   ├── parser.py         # 엑셀/CSV 파싱
│   ├── generator.py      # 폴더/파일 생성
│   ├── validator.py      # 데이터 검증
│   └── templates/        # HTML 템플릿
├── tests/
├── examples/
└── README.md
```

## 개발

```bash
# 테스트 실행
pytest

# 코드 포맷팅
black content_generator/

# Linting
pylint content_generator/
```

## 라이센스

MIT License

## 작성자

메가존 IT 교육팀
