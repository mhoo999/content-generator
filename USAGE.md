# 사용 가이드

## 빠른 시작

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 엑셀 파일 준비

엑셀 파일은 다음 컬럼을 포함해야 합니다:

**필수 컬럼:**
- 과정명
- 차시번호
- 차시명
- 강의영상(mp4) 링크

**선택 컬럼:**
- 챕터구분 (Part 번호)
- 챕터명 (Part 이름)
- 다운로드(zip) 링크

### 3. 실행

```bash
# 기본 사용
python -m content_generator -i your_file.xlsx -o /path/to/output

# 실제 25ctvibec 예시
python -m content_generator \
  -i 25ctvibec.xlsx \
  -o ~/IdeaProjects/contents_it/subjects \
  -t ct2022

# 미리보기만 (실제 생성 안 함)
python -m content_generator -i 25ctvibec.xlsx --dry-run
```

## 엑셀 파일 예시

| 과정명 | 차시 | 챕터구분 | 챕터명 | 차시번호 | 차시명 | 강의영상(mp4) 링크 | 다운로드(zip) 링크 |
|--------|------|----------|--------|----------|--------|-------------------|-------------------|
| AI Vibe ... | 1 | 1 | Part.1 Cursor AI | 01 | DEMO 미리보기 | /cdn-it.../25ctvibec_01.mp4 | /cdn-it.../book_01.zip |
| | 2 | | | 02 | Cursor AI 사용법1 | /cdn-it.../25ctvibec_02.mp4 | |
| | 3 | | | 03 | Cursor AI 사용법2 | /cdn-it.../25ctvibec_03.mp4 | |

**주의:** 같은 값이 반복되는 셀은 비워두거나 병합할 수 있습니다.

## 옵션 설명

### `-i, --input` (필수)
입력 파일 경로 (.xlsx 또는 .csv)

```bash
python -m content_generator -i 25ctvibec.xlsx
```

### `-o, --output` (선택, 기본값: ./output)
출력 디렉토리 경로

```bash
python -m content_generator -i 25ctvibec.xlsx -o ~/projects/subjects
```

### `-t, --template` (선택, 기본값: ct2022)
템플릿 선택
- `ct2022`: 2022 CT 스타일 (자격증 과정, 간단한 구조)
- `it2023`: 2023 IT 스타일 (확장 구조)

```bash
python -m content_generator -i 25itcoms.xlsx -t it2023
```

### `--dry-run` (선택)
실제로 생성하지 않고 미리보기만

```bash
python -m content_generator -i 25ctvibec.xlsx --dry-run
```

### `-v, --verbose` (선택)
상세한 로그 출력

```bash
python -m content_generator -i 25ctvibec.xlsx -v
```

## 생성 결과

```
output/
└── 25ctvibec/
    ├── subjects.json          # 네비게이션 메뉴 데이터
    ├── 01/
    │   ├── index.html         # 뷰어 페이지
    │   └── assets/
    │       └── data/
    │           └── data.json  # 차시 데이터
    ├── 02/
    │   ├── index.html
    │   └── assets/data/data.json
    └── ...
```

## 실무 워크플로우

### 1. 엑셀 시트 받기
교육팀에서 엑셀 파일 수령

### 2. 검증 (dry-run)
```bash
python -m content_generator -i 25ctvibec.xlsx --dry-run
```

생성될 구조 확인

### 3. 실제 생성
```bash
python -m content_generator \
  -i 25ctvibec.xlsx \
  -o ~/IdeaProjects/contents_it/subjects \
  -t ct2022 \
  -v
```

### 4. 확인
```bash
cd ~/IdeaProjects/contents_it
python3 -m http.server 8000

# 브라우저에서
# http://localhost:8000/subjects/25ctvibec/01/
```

### 5. Git 커밋
```bash
cd ~/IdeaProjects/contents_it
git add subjects/25ctvibec/
git commit -m "Add 25ctvibec course structure"
git push
```

## 트러블슈팅

### "필수 컬럼 누락" 에러
엑셀 파일의 컬럼명을 확인하세요. 정확히 일치해야 합니다:
- ✅ `과정명`
- ❌ `과정 명`, `과정이름`

### URL이 `https:/`로 시작
정상입니다. `/cdn-it.livestudy.com/...`을 자동으로 `https:/cdn-it.livestudy.com/...`로 변환합니다.

### 권한 문제
생성된 파일은 자동으로 644 권한으로 설정됩니다.

## 고급 사용

### CSV 파일 사용
엑셀 대신 CSV 파일도 사용 가능합니다:

```bash
# 엑셀을 CSV로 변환
# (엑셀에서 "다른 이름으로 저장" → CSV UTF-8)

python -m content_generator -i 25ctvibec.csv
```

### 여러 과정 일괄 생성
```bash
for file in *.xlsx; do
  python -m content_generator -i "$file" -o ~/projects/subjects
done
```

## 참고

- 생성된 파일을 수동으로 수정하지 마세요
- 수정이 필요하면 엑셀 파일을 수정 후 재생성
- 기존 과정을 덮어쓰기 전에 백업 권장
