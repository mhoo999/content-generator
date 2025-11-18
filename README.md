# Content Generator

교육 콘텐츠 폴더 구조를 자동으로 생성하는 도구입니다.

## 📑 목차

- [빠른 시작](#-빠른-시작-30초)
- [기능](#기능)
- [설치](#설치)
- [사용법](#사용법)
  - [방법 1: 구글 시트 사용 (추천)](#방법-1-구글-시트-사용-추천-)
  - [방법 2: 엑셀 파일 사용](#방법-2-엑셀-파일-사용)
  - [방법 3: CSV 파일 사용](#방법-3-csv-파일-사용)
  - [명령어 옵션 상세 설명](#명령어-옵션-상세-설명)
- [데이터 형식](#데이터-형식-엑셀csv구글-시트)
- [트러블슈팅](#트러블슈팅)
- [FAQ](#faq-자주-묻는-질문)
- [프로젝트 구조](#프로젝트-구조)

---

## ⚡ 빠른 시작 (30초)

### 구글 시트 사용 (추천)

```bash
# 1. 의존성 설치 (최초 1회만)
pip3 install -r requirements.txt

# 2. 구글 시트 공유 링크 복사 후 실행
python3 -m content_generator -i "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

# 완료! 🎉
# output/25ctvibec/ 폴더가 생성됩니다
```

### 엑셀 파일 사용

```bash
# 1. 의존성 설치 (최초 1회만)
pip3 install -r requirements.txt

# 2. 엑셀 파일로 실행
python3 -m content_generator -i ~/Downloads/25ctvibec.xlsx

# 완료! 🎉
```

---

## 기능

- **구글 시트 URL 직접 지원** (다운로드 불필요!)
- 엑셀/CSV 파일에서 과정 데이터 파싱
- 자동으로 폴더 구조 생성
- subjects.json, data.json 자동 생성
- 템플릿 자동 선택 (2022 CT, 2023 IT)
- 데이터 검증

## 설치

```bash
# 의존성 설치
pip3 install -r requirements.txt

# 개발 모드로 설치 (선택)
pip3 install -e .
```

## 사용법

### 방법 1: 구글 시트 사용 (추천 ⭐)

구글 시트를 사용하면 **파일 다운로드 없이** 바로 콘텐츠를 생성할 수 있습니다.

#### Step 1: 구글 시트 준비

1. **구글 시트 열기**
   - 새 구글 시트 생성 또는 기존 시트 사용

2. **데이터 입력** (아래 형식 참고)
   | 과정명 | 차시 | 챕터구분 | 챕터명 | 차시번호 | 차시명 | 강의영상(mp4) 링크 | 다운로드(zip) 링크 |
   |--------|------|----------|--------|----------|--------|-------------------|-------------------|
   | AI Vibe 코딩 | 1 | 1 | Part.1 Cursor AI | 01 | DEMO 미리보기 | //cdn-it.../25ctvibec_01.mp4 | //cdn-it.../book_01.zip |
   | | 2 | | | 02 | Cursor AI 사용법1 | //cdn-it.../25ctvibec_02.mp4 | |
   | | 3 | | | 03 | Cursor AI 사용법2 | //cdn-it.../25ctvibec_03.mp4 | |

3. **공유 설정**
   - 우측 상단 "공유" 버튼 클릭
   - "일반 액세스" → "링크가 있는 모든 사용자"로 변경
   - 권한: "뷰어" (읽기 전용으로 충분)
   - "링크 복사" 클릭

4. **링크 예시**
   ```
   https://docs.google.com/spreadsheets/d/1AbC2dEf3GhI4JkL5MnO6PqR7StU8VwX9YzA/edit#gid=0
   ```

#### Step 2: 명령어 실행

```bash
# 1. 먼저 dry-run으로 미리보기 (실제 생성 안 함)
python -m content_generator \
  -i "https://docs.google.com/spreadsheets/d/1AbC2dEf3GhI4JkL5MnO6PqR7StU8VwX9YzA/edit#gid=0" \
  --dry-run

# 2. 확인 후 실제 생성
python -m content_generator \
  -i "https://docs.google.com/spreadsheets/d/1AbC2dEf3GhI4JkL5MnO6PqR7StU8VwX9YzA/edit#gid=0" \
  -o ~/IdeaProjects/contents_it/subjects \
  -t ct2022

# 3. 상세 로그와 함께 실행
python -m content_generator \
  -i "https://docs.google.com/spreadsheets/d/SHEET_ID/edit" \
  -o ~/IdeaProjects/contents_it/subjects \
  -v
```

#### Step 3: 결과 확인

```bash
# 생성된 폴더로 이동
cd ~/IdeaProjects/contents_it/subjects/25ctvibec

# 파일 확인
ls -la
# subjects.json
# 01/
# 02/
# 03/
# ...

# 로컬 서버로 테스트
cd ~/IdeaProjects/contents_it
python3 -m http.server 8000

# 브라우저에서 확인
# http://localhost:8000/subjects/25ctvibec/01/
```

---

### 방법 2: 엑셀 파일 사용

엑셀 파일을 로컬에 다운로드한 경우 사용합니다.

#### Step 1: 엑셀 파일 준비

1. **엑셀 파일 다운로드**
   - 구글 시트: 파일 → 다운로드 → Microsoft Excel (.xlsx)
   - 또는 교육팀에서 받은 .xlsx 파일 사용

2. **파일 위치 확인**
   ```bash
   # 예시: Downloads 폴더
   ls ~/Downloads/25ctvibec.xlsx
   ```

#### Step 2: 명령어 실행

```bash
# 기본 사용 (첫 번째 시트 사용)
python -m content_generator -i ~/Downloads/25ctvibec.xlsx

# 특정 시트 탭 선택 (시트 이름으로)
python -m content_generator -i ~/Downloads/25ctvibec.xlsx -s "25ctvibec"

# 특정 시트 탭 선택 (인덱스로, 0부터 시작)
python -m content_generator -i ~/Downloads/25ctvibec.xlsx -s 1

# 출력 디렉토리 지정
python -m content_generator \
  -i ~/Downloads/25ctvibec.xlsx \
  -s "25ctvibec" \
  -o ~/IdeaProjects/contents_it/subjects

# 템플릿 선택 (ct2022 또는 it2023)
python -m content_generator \
  -i ~/Downloads/25ctvibec.xlsx \
  -s "25ctvibec" \
  -o ~/IdeaProjects/contents_it/subjects \
  -t ct2022
```

---

### 방법 3: CSV 파일 사용

```bash
# CSV 파일도 동일하게 사용 가능
python -m content_generator -i ~/Downloads/25ctvibec.csv -o ./output
```

---

### 명령어 옵션 상세 설명

| 옵션 | 짧은 형식 | 필수 | 기본값 | 설명 |
|------|----------|------|--------|------|
| `--input` | `-i` | ✅ | - | 입력 소스 (구글 시트 URL, 엑셀, CSV) |
| `--output` | `-o` | ❌ | `./output` | 출력 디렉토리 경로 |
| `--template` | `-t` | ❌ | `ct2022` | 템플릿 종류 (`ct2022`, `it2023`, `auto`) |
| `--sheet` | `-s` | ❌ | 첫 번째 시트 | 엑셀 시트 이름 또는 인덱스 (예: `"Sheet1"`, `0`) |
| `--dry-run` | - | ❌ | - | 실제 생성 없이 미리보기만 |
| `--verbose` | `-v` | ❌ | - | 상세 로그 출력 |

#### 옵션 예시

```bash
# 최소 명령어 (입력만 지정)
python -m content_generator -i "GOOGLE_SHEET_URL"
# → output/25ctvibec/ 폴더에 생성됨

# 출력 경로 지정
python -m content_generator -i "URL" -o ~/projects/subjects
# → ~/projects/subjects/25ctvibec/ 폴더에 생성됨

# 템플릿 선택
python -m content_generator -i "URL" -t it2023
# → IT 2023 스타일 템플릿 사용

# 특정 시트 선택 (시트 이름)
python -m content_generator -i file.xlsx -s "25ctvibec"
# → "25ctvibec" 시트 사용

# 특정 시트 선택 (인덱스, 0부터 시작)
python -m content_generator -i file.xlsx -s 1
# → 두 번째 시트 사용

# 미리보기 (파일 생성 안 함)
python -m content_generator -i "URL" --dry-run
# → 생성될 구조만 출력

# 상세 로그
python -m content_generator -i "URL" -v
# → 과정 코드, 과정명, 차시 수 등 상세 정보 출력
```

---

### 실행 결과 예시

#### 성공 시 출력

```
============================================================
📚 Content Generator v1.0.0
============================================================

📊 구글 시트에서 데이터 가져오는 중...
📖 데이터 파싱 중: https://docs.google.com/spreadsheets/d/...
   - 과정 코드: 25ctvibec
   - 과정명: AI Vibe (바이브) 코딩으로 크롬 확장 프로그램 만들기
   - 총 차시: 22
   - 챕터 수: 5
✅ 파싱 완료

📁 폴더 생성 중...
✅ 폴더 생성 완료

📄 파일 생성 중...
   - subjects.json
   - 01/index.html, 01/assets/data/data.json
   - 02/index.html, 02/assets/data/data.json
   ...
✅ 파일 생성 완료

============================================================
🎉 성공! 25ctvibec 생성 완료
📂 위치: /Users/username/projects/contents_it/subjects/25ctvibec
============================================================
```

#### 생성된 폴더 구조

```
subjects/
└── 25ctvibec/
    ├── subjects.json           # 네비게이션 메뉴 데이터
    ├── 01/
    │   ├── index.html          # 차시 뷰어 페이지
    │   └── assets/
    │       └── data/
    │           └── data.json   # 차시별 데이터 (영상 URL, 다운로드 링크 등)
    ├── 02/
    │   ├── index.html
    │   └── assets/data/data.json
    ├── 03/
    │   ├── index.html
    │   └── assets/data/data.json
    └── ...
```

## 데이터 형식 (엑셀/CSV/구글 시트)

### 필수 컬럼

| 컬럼명 | 설명 | 예시 | 비고 |
|--------|------|------|------|
| **과정명** | 교육 과정 이름 | AI Vibe 코딩으로 크롬 확장 프로그램 만들기 | 첫 행 값이 모든 행에 적용됨 |
| **차시번호** | 차시 번호 (숫자) | 01, 02, 03, ... | 01~99 형식 권장 |
| **차시명** | 차시 제목 | DEMO 미리보기 | 각 차시마다 필수 |
| **강의영상(mp4) 링크** | 동영상 파일 URL | //cdn-it.livestudy.com/mov/2025/25ctvibec/25ctvibec_01.mp4 | https:// 또는 // 형식 |

### 선택 컬럼

| 컬럼명 | 설명 | 예시 | 비고 |
|--------|------|------|------|
| **챕터구분** | Part/Chapter 번호 | 1, 2, 3 | 챕터로 구분할 경우 사용 |
| **챕터명** | Part/Chapter 이름 | Part.1 Cursor AI 시작하기 | 챕터구분과 함께 사용 |
| **다운로드(zip) 링크** | 실습 파일 다운로드 URL | //cdn-it.livestudy.com/.../book_01.zip | 선택 사항 |

### 데이터 입력 예시

#### 전체 예시

| 과정명 | 차시 | 챕터구분 | 챕터명 | 차시번호 | 차시명 | 강의영상(mp4) 링크 | 다운로드(zip) 링크 |
|--------|------|----------|--------|----------|--------|-------------------|-------------------|
| AI Vibe (바이브) 코딩으로 크롬 확장 프로그램 만들기 | 1 | 1 | Part.1 Cursor AI 시작하기 | 01 | DEMO 미리보기 | //cdn-it.livestudy.com/mov/2025/25ctvibec/25ctvibec_01.mp4 | //cdn-it.livestudy.com/mov/2025/25ctvibec/book_01.zip |
| | 2 | | | 02 | Cursor AI 설치 및 설정 | //cdn-it.livestudy.com/mov/2025/25ctvibec/25ctvibec_02.mp4 | |
| | 3 | | | 03 | AI 코딩 보조 기능 사용법 | //cdn-it.livestudy.com/mov/2025/25ctvibec/25ctvibec_03.mp4 | //cdn-it.livestudy.com/mov/2025/25ctvibec/book_03.zip |
| | 4 | 2 | Part.2 크롬 확장 프로그램 개발 | 04 | 확장 프로그램 구조 이해 | //cdn-it.livestudy.com/mov/2025/25ctvibec/25ctvibec_04.mp4 | |
| | 5 | | | 05 | Manifest 파일 작성 | //cdn-it.livestudy.com/mov/2025/25ctvibec/25ctvibec_05.mp4 | //cdn-it.livestudy.com/mov/2025/25ctvibec/book_05.zip |

#### 입력 팁

1. **반복되는 값 생략 가능**
   - "과정명", "챕터구분", "챕터명"은 빈 셀로 두면 자동으로 위 값 사용
   - 엑셀에서 셀 병합해도 됨

2. **URL 형식**
   - `https://cdn-it.livestudy.com/...` ✅
   - `//cdn-it.livestudy.com/...` ✅ (자동으로 https:// 추가됨)
   - `/cdn-it.livestudy.com/...` ✅ (자동으로 https: 추가됨)

3. **차시번호 형식**
   - 숫자만: `1`, `2`, `3` → 자동으로 `01`, `02`, `03` 변환
   - 두 자리: `01`, `02`, `03` ✅ (권장)

4. **다운로드 링크**
   - 다운로드 파일이 없는 차시는 비워두면 됨
   - 있는 차시만 입력

### 구글 시트 템플릿

빠르게 시작하려면 아래 템플릿을 복사해서 사용하세요:

```
과정명 | 차시 | 챕터구분 | 챕터명 | 차시번호 | 차시명 | 강의영상(mp4) 링크 | 다운로드(zip) 링크
-------|------|----------|--------|----------|--------|-------------------|-------------------
[과정명 입력] | 1 | 1 | Part.1 [챕터명] | 01 | [차시명 입력] | //cdn-it.livestudy.com/mov/2025/[과정코드]/[과정코드]_01.mp4 |
```

## 트러블슈팅

### 자주 발생하는 오류

#### 1. "필수 컬럼 누락" 오류

```
❌ 오류: 필수 컬럼 누락: 과정명, 차시번호
```

**해결 방법:**
- 엑셀/구글 시트의 컬럼명을 정확히 확인하세요
- 컬럼명은 **정확히 일치**해야 합니다:
  - ✅ `과정명` (올바름)
  - ❌ `과정 명`, `과정이름` (잘못됨)
  - ✅ `차시번호` (올바름)
  - ❌ `차시 번호`, `차시No` (잘못됨)

#### 2. "URL에서 데이터를 가져올 수 없습니다" 오류

```
❌ 오류: URL에서 데이터를 가져올 수 없습니다: 403 Forbidden
```

**해결 방법:**
- 구글 시트 공유 설정을 확인하세요:
  1. 구글 시트 → 우측 상단 "공유" 버튼
  2. "일반 액세스" → "링크가 있는 모든 사용자"
  3. 권한: "뷰어" 이상

#### 3. "파일을 찾을 수 없습니다" 오류

```
❌ 오류: 파일을 찾을 수 없습니다: 25ctvibec.xlsx
```

**해결 방법:**
- 파일 경로를 절대 경로로 지정하세요:
  ```bash
  # ❌ 잘못된 경로
  python -m content_generator -i 25ctvibec.xlsx

  # ✅ 올바른 경로
  python -m content_generator -i ~/Downloads/25ctvibec.xlsx
  ```

#### 4. "과정 코드를 추출할 수 없습니다" 경고

**해결 방법:**
- 강의영상 URL 형식을 확인하세요:
  ```
  ✅ 올바른 형식:
  //cdn-it.livestudy.com/mov/2025/25ctvibec/25ctvibec_01.mp4

  ❌ 잘못된 형식:
  example.com/video.mp4
  ```

### FAQ (자주 묻는 질문)

#### Q1. 구글 시트를 수정하면 자동으로 반영되나요?

A: 네! 구글 시트를 수정한 후 명령어를 다시 실행하면 최신 데이터로 생성됩니다. 파일을 다시 다운로드할 필요가 없습니다.

```bash
# 구글 시트 수정 후 그냥 다시 실행
python -m content_generator -i "GOOGLE_SHEET_URL" -o ~/projects/subjects
```

#### Q2. 엑셀 파일의 여러 시트(탭) 중 특정 시트만 선택할 수 있나요?

A: 네! `-s` 또는 `--sheet` 옵션으로 특정 시트를 선택할 수 있습니다.

**방법 1: 시트 이름으로 선택**
```bash
python -m content_generator -i file.xlsx -s "25ctvibec"
```

**방법 2: 인덱스로 선택 (0부터 시작)**
```bash
# 첫 번째 시트 (기본값)
python -m content_generator -i file.xlsx -s 0

# 두 번째 시트
python -m content_generator -i file.xlsx -s 1

# 세 번째 시트
python -m content_generator -i file.xlsx -s 2
```

**시트가 없는 경우:**
존재하지 않는 시트를 지정하면 사용 가능한 시트 목록이 표시됩니다:
```
❌ 오류: 시트를 찾을 수 없습니다: Sheet99
사용 가능한 시트: '25ctvibec', '25itcoms', 'Sheet1'
```

**구글 시트 URL의 경우:**
URL의 `gid` 파라미터를 변경하세요:
```bash
# 첫 번째 시트 (gid=0, 기본값)
python -m content_generator -i "https://docs.google.com/spreadsheets/d/SHEET_ID/edit#gid=0"

# 두 번째 시트 (gid 확인 필요)
python -m content_generator -i "https://docs.google.com/spreadsheets/d/SHEET_ID/edit#gid=123456789"
```

**gid 확인 방법:** 구글 시트에서 탭을 클릭하면 URL에 `#gid=숫자` 형태로 표시됩니다.

#### Q3. 기존 폴더가 있으면 덮어쓰나요?

A: 네, 기존 폴더는 **덮어쓰기** 됩니다. 백업이 필요한 경우 미리 복사하세요:

```bash
# 백업 생성
cp -r ~/projects/subjects/25ctvibec ~/projects/subjects/25ctvibec_backup

# 생성 실행
python -m content_generator -i "URL" -o ~/projects/subjects
```

#### Q4. 엑셀과 구글 시트 중 뭐가 더 좋나요?

A: **구글 시트를 추천**합니다:

| 구분 | 구글 시트 | 엑셀 파일 |
|------|-----------|----------|
| 다운로드 | 불필요 ✅ | 필요 ❌ |
| 수정 반영 | 즉시 ✅ | 다시 다운로드 필요 ❌ |
| 공동 작업 | 가능 ✅ | 어려움 ❌ |
| 버전 관리 | 자동 ✅ | 수동 ❌ |

#### Q5. ct2022와 it2023 템플릿 차이는?

A: 템플릿에 따라 생성되는 HTML 구조가 다릅니다:

- **ct2022**: 2022 CT 자격증 과정용 (간단한 구조)
- **it2023**: 2023 IT 교육용 (확장된 구조)
- **auto**: URL에서 자동 감지 (25ct* → ct2022, 25it* → it2023)

```bash
# 자동 감지 (추천)
python -m content_generator -i "URL" -t auto

# 수동 지정
python -m content_generator -i "URL" -t ct2022
```

#### Q6. 차시 순서를 변경하려면?

A: 구글 시트에서 행 순서를 변경하고 다시 실행하세요. 차시번호 컬럼은 그대로 두고 행만 이동하면 됩니다.

#### Q7. 다운로드 링크가 없는 차시는 어떻게 하나요?

A: "다운로드(zip) 링크" 컬럼을 비워두면 됩니다. 해당 차시는 다운로드 버튼이 표시되지 않습니다.

## 프로젝트 구조

```
content-generator/
├── content_generator/
│   ├── __init__.py
│   ├── __main__.py       # CLI 진입점
│   ├── parser.py         # 엑셀/CSV/URL 파싱
│   ├── generator.py      # 폴더/파일 생성
│   └── templates/        # HTML 템플릿
├── tests/
├── examples/
│   └── test_25ctvibec.xlsx
├── requirements.txt
├── README.md
├── USAGE.md
└── setup.py
```

## 개발

```bash
# 의존성 설치
pip install -r requirements.txt

# 개발 모드로 설치
pip install -e .

# 예시 파일로 테스트
python -m content_generator -i examples/test_25ctvibec.xlsx --dry-run
```

## 라이센스

MIT License

## 작성자

메가존 IT 교육팀
