"""
컨텐츠 폴더 구조 생성 모듈
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ContentGenerator:
    """컨텐츠 생성기"""

    def __init__(self, course_data: Dict, output_dir: str, template: str = "ct2022", input_file: str = None):
        """
        Args:
            course_data: 파싱된 과정 데이터
            output_dir: 출력 디렉토리
            template: 템플릿 종류 (ct2022, it2023)
            input_file: 입력 파일 경로 (문서화용)
        """
        self.course_data = course_data
        self.output_dir = Path(output_dir)
        self.template = template
        self.course_code = course_data['course_code']
        self.course_dir = self.output_dir / self.course_code
        self.input_file = input_file

    def generate(self, dry_run: bool = False):
        """
        폴더 구조 생성

        Args:
            dry_run: True면 실제 생성하지 않고 미리보기만
        """
        print(f"📁 생성할 과정: {self.course_code}")
        print(f"📝 과정명: {self.course_data['subject']}")
        print(f"📊 총 차시: {self.course_data['total_lessons']}")
        print(f"🎨 템플릿: {self.template}")
        print(f"📂 출력 경로: {self.course_dir}")
        print()

        if dry_run:
            print("🔍 [DRY RUN] 실제 생성 없이 미리보기:")
            self._preview_structure()
            return

        # 실제 생성
        self._create_course_structure()
        self._create_subjects_json()
        self._create_lesson_files()
        self._create_generation_log()

        print(f"\n✅ 완료! {self.course_code} 생성됨")

    def _preview_structure(self):
        """생성될 구조 미리보기"""
        print(f"{self.course_code}/")
        print(f"├── subjects.json")

        for lesson in self.course_data['lessons']:
            lesson_num = lesson['number']
            print(f"├── {lesson_num}/")
            print(f"│   ├── index.html")
            print(f"│   └── assets/data/data.json")

    def _create_course_structure(self):
        """과정 폴더 구조 생성"""
        # 과정 루트 디렉토리
        self.course_dir.mkdir(parents=True, exist_ok=True)

        # 각 차시 폴더
        for lesson in self.course_data['lessons']:
            lesson_dir = self.course_dir / lesson['number']
            lesson_dir.mkdir(exist_ok=True)

            # assets/data 폴더
            data_dir = lesson_dir / 'assets' / 'data'
            data_dir.mkdir(parents=True, exist_ok=True)

        print(f"✅ 폴더 구조 생성 완료")

    def _create_subjects_json(self):
        """subjects.json 생성"""
        # 각 차시마다 별도의 subject로 생성 (25itcoms 형식)
        subjects = []

        for lesson in self.course_data['lessons']:
            # "차시" 값이 있으면 "1차", "2차" 형식으로, 없으면 차시번호 사용
            if lesson.get('order'):
                title_prefix = f"{lesson['order']}차"
            else:
                title_prefix = f"{lesson['index']}차"

            subjects.append({
                "title": f"{title_prefix} {lesson['title']}",
                "lists": [f"{lesson['number']} {lesson['title']}"]
            })

        subjects_data = {"subjects": subjects}

        # 파일 저장
        subjects_file = self.course_dir / 'subjects.json'
        with open(subjects_file, 'w', encoding='utf-8') as f:
            json.dump(subjects_data, f, ensure_ascii=False, indent='\t')

        subjects_file.chmod(0o644)
        print(f"✅ subjects.json 생성 완료")

    def _get_lesson_title(self, lesson_num: str) -> str:
        """차시 번호로 차시명 찾기"""
        for lesson in self.course_data['lessons']:
            if lesson['number'] == lesson_num:
                return lesson['title']
        return ""

    def _create_lesson_files(self):
        """각 차시별 파일 생성"""
        for lesson in self.course_data['lessons']:
            lesson_dir = self.course_dir / lesson['number']

            # index.html 생성
            self._create_index_html(lesson_dir)

            # data.json 생성
            self._create_data_json(lesson_dir, lesson)

        # 권한 설정
        self._set_permissions()

        print(f"✅ {len(self.course_data['lessons'])}개 차시 파일 생성 완료")

    def _create_index_html(self, lesson_dir: Path):
        """index.html 생성 (템플릿 기반)"""
        template_html = self._get_template_html()

        index_file = lesson_dir / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(template_html)

    def _get_template_html(self) -> str:
        """템플릿 HTML 반환"""
        if self.template == "ct2022":
            return self._get_ct2022_template()
        elif self.template == "it2023":
            return self._get_it2023_template()
        else:
            # 기본 템플릿
            return self._get_ct2022_template()

    def _get_ct2022_template(self) -> str:
        """2022 CT 템플릿"""
        return '''<!DOCTYPE html>
<html lang="ko">
<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, user-scalable=no" />
\t<meta http-equiv="X-UA-Compatible" content="ie=edge">
\t<title>메가존아이티평생교육원</title>
\t<script src="../../../resources/scripts/jquery/jquery.js"></script>
\t<script src="../../../resources/scripts/vue/vue.min.js"></script>
\t<script src="../../../resources/scripts/vue/vue-router.min.js"></script>

\t<script src="../../../resources/scripts/2022/templates/layout_ct.js"></script>
\t<script src="../../../resources/scripts/2022/templates/defaults.js"></script>
\t<script src="../../../resources/scripts/sync.js"></script>

\t<link rel="stylesheet" href="../../../resources/scripts/videojs/video-js.min.css">


\t<link rel="stylesheet" href="../../../resources/styles/2022/base.css">
\t<link rel="stylesheet" href="../../../resources/styles/2022/layout.css">
\t<link rel="stylesheet" href="../../../resources/styles/2022/modules.css">
\t<link rel="stylesheet" href="../../../resources/styles/2022/mediaquery.css">
\t<link rel="stylesheet" href="../../../resources/styles/2022/type-2.css">

\t<link rel="stylesheet" media="print" type="text/css" href="../../../resources/styles/print.css">
</head>
<body>
\t<div id="app"></div>
\t<script src="../../../resources/scripts/app.js"></script>
\t<script src="../../../resources/scripts/videojs/video.min.js"></script>

\t<script src="../../../resources/scripts/2022/commons_ct.js"></script>
\t<script src="../../../resources/scripts/videojs/videojs-contrib-hls.min.js"></script>
\t<script src="../../../resources/scripts/videojs/videojs.hotkeys.min.js"></script>
</body>
</html>'''

    def _get_it2023_template(self) -> str:
        """2023 IT 템플릿"""
        return '''<!DOCTYPE html>
<html lang="ko">
<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, user-scalable=no" />
\t<meta http-equiv="X-UA-Compatible" content="ie=edge">
\t<title>메가존아이티평생교육원</title>
\t<script src="../../../resources/scripts/jquery/jquery.js"></script>
\t<script src="../../../resources/scripts/vue/vue.min.js"></script>
\t<script src="../../../resources/scripts/vue/vue-router.min.js"></script>

\t<script src="../../../resources/scripts/2022/templates/layout.js"></script>
\t<script src="../../../resources/scripts/2022/templates/defaults.js"></script>
\t<script src="../../../resources/scripts/sync.js"></script>

\t<link rel="stylesheet" href="../../../resources/scripts/videojs/video-js.min.css">

\t<link rel="stylesheet" href="../../../resources/styles/2023/base.css">
\t<link rel="stylesheet" href="../../../resources/styles/2025/layout.css">
\t<link rel="stylesheet" href="../../../resources/styles/2023/modules.css">
\t<link rel="stylesheet" href="../../../resources/styles/2023/mediaquery.css">
\t<link rel="stylesheet" href="../../../resources/styles/2023/type-1.css">

\t<link rel="stylesheet" media="print" type="text/css" href="../../../resources/styles/print.css">
</head>
<body>
<div id="app"></div>
<script src="../../../resources/scripts/app.js"></script>
<script src="../../../resources/scripts/videojs/video.min.js"></script>

<script src="../../../resources/scripts/2022/commons.js"></script>
<script src="../../../resources/scripts/videojs/videojs-contrib-hls.min.js"></script>
<script src="../../../resources/scripts/videojs/videojs.hotkeys.min.js"></script>
</body>
</html>'''

    def _create_data_json(self, lesson_dir: Path, lesson: Dict):
        """data.json 생성"""
        data = {
            "subject": self.course_data['subject'],
            "index": lesson['index'],
            "section": 1,
            "sections": ["학습하기"],
            "pages": [
                {
                    "path": "/lecture",
                    "section": 1,
                    "title": "학습하기",
                    "component": "lecture",
                    "media": lesson['video_url'],
                    "data": {}
                }
            ]
        }

        # guide 필드 추가 (다운로드 자료가 있으면)
        if lesson['download_url']:
            data['guide'] = lesson['download_url']
        else:
            # ct2022 템플릿은 guide 필드 필수
            if self.template == "ct2022":
                # Part별로 다운로드 자료 공유
                data['guide'] = self._get_guide_for_lesson(lesson['index'])

        # 파일 저장
        data_file = lesson_dir / 'assets' / 'data' / 'data.json'
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')

    def _get_guide_for_lesson(self, lesson_index: int) -> str:
        """차시에 맞는 guide URL 반환"""
        # 현재 차시가 속한 Part를 찾아서 해당 Part의 첫 차시 다운로드 URL 사용
        current_chapter = None

        # 역순으로 순회하여 lesson_start가 lesson_index 이하인 가장 가까운 chapter 찾기
        for chapter in reversed(self.course_data['chapters']):
            if chapter['lesson_start'] <= lesson_index:
                current_chapter = chapter
                break

        if current_chapter:
            # 해당 Part의 첫 차시에서 다운로드 URL 찾기
            first_lesson_num = current_chapter['lessons'][0]
            for lesson in self.course_data['lessons']:
                if lesson['number'] == first_lesson_num and lesson['download_url']:
                    return lesson['download_url']

        # 찾지 못한 경우 첫 번째 다운로드 URL 사용
        for lesson in self.course_data['lessons']:
            if lesson['download_url']:
                return lesson['download_url']

        # 그래도 없으면 빈 문자열
        return ""

    def _set_permissions(self):
        """파일 권한 설정 (644)"""
        for lesson in self.course_data['lessons']:
            lesson_dir = self.course_dir / lesson['number']

            # index.html
            index_file = lesson_dir / 'index.html'
            if index_file.exists():
                index_file.chmod(0o644)

            # data.json
            data_file = lesson_dir / 'assets' / 'data' / 'data.json'
            if data_file.exists():
                data_file.chmod(0o644)

    def _create_generation_log(self):
        """생성 이력 로그 파일 생성 (레포지토리 폴더)"""
        # 레포지토리 루트 경로 찾기 (__file__의 2단계 상위)
        repo_root = Path(__file__).parent.parent
        history_dir = repo_root / 'history'
        history_dir.mkdir(parents=True, exist_ok=True)

        # 현재 날짜+시간으로 파일명 생성 (YYMMDD_HHMM.json)
        now = datetime.now()
        filename = now.strftime('%y%m%d_%H%M.json')  # 예: 251119_1007.json
        history_file = history_dir / filename

        # 이력 데이터 (간략한 정보만)
        log_data = {
            "generated_at": now.isoformat(),
            "course_code": self.course_code,
            "subject": self.course_data['subject'],
            "total_lessons": self.course_data['total_lessons'],
            "chapters": len(self.course_data['chapters']),
            "template": self.template,
            "input_file": self.input_file,
            "output_dir": str(self.course_dir),
            "lessons": [
                {
                    "number": lesson['number'],
                    "title": lesson['title'],
                    "video_url": lesson['video_url'],
                    "download_url": lesson['download_url'] or self._get_guide_for_lesson(lesson['index'])
                }
                for lesson in self.course_data['lessons']
            ]
        }

        # 파일 저장
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)

        history_file.chmod(0o644)
        print(f"📝 생성 이력 저장: {history_file}")
