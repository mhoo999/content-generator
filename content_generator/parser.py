"""
엑셀/CSV 파일 파싱 모듈
"""

import pandas as pd
import requests
import re
from pathlib import Path
from typing import Dict, List, Optional
from io import BytesIO


class CourseDataParser:
    """과정 데이터 파서"""

    # 컬럼 매핑 (엑셀 컬럼명 → 내부 필드명)
    COLUMN_MAPPING = {
        '과정명': 'subject',
        '차시': 'lesson_order',
        '챕터구분': 'chapter_number',
        '챕터명': 'chapter_name',
        '강의 수': 'lecture_count',
        '차시번호': 'lesson_number',
        '차시명': 'lesson_title',
        '학습자페이지 노출 차시명': 'lesson_display_title',
        '강의영상(mp4) 링크': 'video_url',
        '다운로드(zip) 링크': 'download_url',
    }

    REQUIRED_COLUMNS = ['과정명', '차시번호', '차시명', '강의영상(mp4) 링크']

    def __init__(self, file_path: str):
        """
        Args:
            file_path: 엑셀/CSV 파일 경로 또는 구글 시트 URL
        """
        self.file_path_or_url = file_path
        self.is_url = self._is_url(file_path)
        self.file_path = None if self.is_url else Path(file_path)
        self.df: Optional[pd.DataFrame] = None
        self.course_code: Optional[str] = None

    @staticmethod
    def _is_url(path: str) -> bool:
        """URL인지 확인"""
        return path.startswith('http://') or path.startswith('https://')

    @staticmethod
    def _convert_google_sheets_url(url: str) -> str:
        """
        구글 시트 URL을 CSV export URL로 변환

        입력 예시:
        - https://docs.google.com/spreadsheets/d/SHEET_ID/edit#gid=0
        - https://docs.google.com/spreadsheets/d/SHEET_ID/edit?usp=sharing

        출력:
        - https://docs.google.com/spreadsheets/d/SHEET_ID/export?format=csv&gid=0
        """
        # SHEET_ID 추출
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
        if not match:
            return url  # 구글 시트가 아니면 원본 반환

        sheet_id = match.group(1)

        # GID 추출 (시트 탭 번호, 기본값 0)
        gid_match = re.search(r'[#&]gid=(\d+)', url)
        gid = gid_match.group(1) if gid_match else '0'

        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    def parse(self) -> Dict:
        """
        파일 또는 URL을 파싱하여 과정 데이터 반환

        Returns:
            {
                'course_code': '25ctvibec',
                'subject': '과정명',
                'chapters': [
                    {
                        'number': 1,
                        'name': 'Part.1 ...',
                        'lessons': [...]
                    }
                ],
                'lessons': [...],
                'total_lessons': 22
            }
        """
        # 데이터 읽기
        if self.is_url:
            self._load_from_url()
        else:
            self._load_from_file()

        # 컬럼 검증
        self._validate_columns()

        # 데이터 정리
        self._clean_data()

        # 파싱
        course_data = self._parse_course_data()

        return course_data

    def _load_from_url(self):
        """URL에서 데이터 로드"""
        url = self.file_path_or_url

        # 구글 시트 URL이면 CSV export URL로 변환
        if 'docs.google.com/spreadsheets' in url:
            url = self._convert_google_sheets_url(url)
            print(f"📊 구글 시트에서 데이터 가져오는 중...")

        # URL에서 데이터 다운로드
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"URL에서 데이터를 가져올 수 없습니다: {e}")

        # CSV로 파싱
        try:
            self.df = pd.read_csv(BytesIO(response.content))
        except Exception as e:
            raise ValueError(f"CSV 파싱 실패: {e}")

    def _load_from_file(self):
        """파일에서 데이터 로드"""
        if self.file_path.suffix == '.xlsx':
            self.df = pd.read_excel(self.file_path)
        elif self.file_path.suffix == '.csv':
            self.df = pd.read_csv(self.file_path)
        else:
            raise ValueError(f"지원하지 않는 파일 형식: {self.file_path.suffix}")

    def _validate_columns(self):
        """필수 컬럼 확인"""
        missing_columns = []
        for col in self.REQUIRED_COLUMNS:
            if col not in self.df.columns:
                missing_columns.append(col)

        if missing_columns:
            raise ValueError(f"필수 컬럼 누락: {', '.join(missing_columns)}")

    def _clean_data(self):
        """데이터 정리 (빈 셀 채우기)"""
        # 과정명: 첫 번째 행 값으로 모두 채우기
        if '과정명' in self.df.columns:
            first_subject = self.df['과정명'].iloc[0]
            self.df['과정명'] = self.df['과정명'].fillna(first_subject)

        # 챕터 정보: 이전 행 값으로 채우기 (forward fill)
        if '챕터구분' in self.df.columns:
            self.df['챕터구분'] = self.df['챕터구분'].ffill()
        if '챕터명' in self.df.columns:
            self.df['챕터명'] = self.df['챕터명'].ffill()

        # NaN을 None으로 변환
        self.df = self.df.where(pd.notnull(self.df), None)

    def _parse_course_data(self) -> Dict:
        """과정 데이터 파싱"""
        # 과정명 추출
        subject = self.df['과정명'].iloc[0]

        # 차시 데이터 추출
        lessons = []
        chapters = []
        current_chapter = None

        for idx, row in self.df.iterrows():
            # 차시 데이터
            lesson = {
                'index': int(row['차시번호']) if pd.notna(row['차시번호']) else idx + 1,
                'number': f"{int(row['차시번호']):02d}" if pd.notna(row['차시번호']) else f"{idx + 1:02d}",
                'title': row['차시명'],
                'video_url': self._normalize_url(row['강의영상(mp4) 링크']),
                'download_url': self._normalize_url(row.get('다운로드(zip) 링크')),
            }
            lessons.append(lesson)

            # 챕터 정보 (챕터구분이 변경될 때)
            if '챕터구분' in row and pd.notna(row['챕터구분']):
                chapter_num = int(row['챕터구분'])
                if current_chapter is None or current_chapter['number'] != chapter_num:
                    current_chapter = {
                        'number': chapter_num,
                        'name': row.get('챕터명', f'Part.{chapter_num}'),
                        'lesson_start': lesson['index'],
                        'lessons': []
                    }
                    chapters.append(current_chapter)

            if current_chapter:
                current_chapter['lessons'].append(lesson['number'])

        # 과정 코드 추출 (강의영상 링크에서)
        if lessons:
            video_url = lessons[0]['video_url']
            # 예: https://cdn-it.livestudy.com/mov/2025/25ctvibec/25ctvibec_01.mp4
            # → 25ctvibec
            parts = video_url.split('/')
            for i, part in enumerate(parts):
                if part.isdigit() and len(part) == 4:  # 년도 (2025)
                    if i + 1 < len(parts):
                        self.course_code = parts[i + 1]
                        break

        return {
            'course_code': self.course_code,
            'subject': subject,
            'chapters': chapters,
            'lessons': lessons,
            'total_lessons': len(lessons)
        }

    def _normalize_url(self, url: Optional[str]) -> Optional[str]:
        """URL 정규화 (https:// 추가)"""
        if not url:
            return None

        url = str(url).strip()
        if url.startswith('/'):
            return f"https:{url}"
        elif not url.startswith('http'):
            return f"https://{url}"
        return url


def parse_course_file(file_path: str) -> Dict:
    """
    과정 파일 파싱 (헬퍼 함수)

    Args:
        file_path: 엑셀 또는 CSV 파일 경로

    Returns:
        파싱된 과정 데이터
    """
    parser = CourseDataParser(file_path)
    return parser.parse()
