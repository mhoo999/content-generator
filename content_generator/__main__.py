"""
CLI 진입점
"""

import argparse
import sys
from pathlib import Path

from .parser import parse_course_file
from .generator import ContentGenerator


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='교육 콘텐츠 폴더 구조 자동 생성 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
사용 예시:
  # 엑셀 파일에서 생성
  python -m content_generator -i 25ctvibec.xlsx -o ~/projects/contents_it/subjects

  # 구글 시트 링크로 바로 생성 (다운로드 불필요!)
  python -m content_generator -i "https://docs.google.com/spreadsheets/d/SHEET_ID/edit#gid=0"

  # 특정 시트 탭 선택 (시트 이름으로)
  python -m content_generator -i 25ctvibec.xlsx -s "25ctvibec"

  # 특정 시트 탭 선택 (인덱스로, 0부터 시작)
  python -m content_generator -i 25ctvibec.xlsx -s 1

  # 템플릿 지정
  python -m content_generator -i 25ctvibec.xlsx -t ct2022

  # 미리보기만 (실제 생성 안 함)
  python -m content_generator -i "https://docs.google.com/spreadsheets/d/SHEET_ID/edit" --dry-run
        '''
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='입력 파일 (엑셀, CSV) 또는 구글 시트 URL'
    )

    parser.add_argument(
        '-o', '--output',
        default='./output',
        help='출력 디렉토리 (기본: ./output)'
    )

    parser.add_argument(
        '-t', '--template',
        choices=['ct2022', 'it2023', 'auto'],
        default='ct2022',
        help='템플릿 선택 (기본: ct2022)'
    )

    parser.add_argument(
        '-s', '--sheet',
        help='엑셀 시트 이름 또는 인덱스 (기본: 첫 번째 시트). 예: "Sheet1" 또는 "0"'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='실제 생성 없이 미리보기만'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='상세 로그 출력'
    )

    args = parser.parse_args()

    # 입력 확인 (URL이 아닌 경우 파일 존재 확인)
    is_url = args.input.startswith('http://') or args.input.startswith('https://')
    if not is_url:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ 오류: 파일을 찾을 수 없습니다: {args.input}")
            sys.exit(1)

    try:
        print("=" * 60)
        print("📚 Content Generator v1.0.0")
        print("=" * 60)
        print()

        # 1. 파싱
        input_name = args.input if is_url else Path(args.input).name
        print(f"📖 데이터 파싱 중: {input_name}")

        # 시트 이름 처리 (숫자 문자열을 int로 변환)
        sheet_name = args.sheet
        if sheet_name and sheet_name.isdigit():
            sheet_name = int(sheet_name)

        course_data = parse_course_file(args.input, sheet_name)

        if args.verbose:
            print(f"   - 과정 코드: {course_data['course_code']}")
            print(f"   - 과정명: {course_data['subject']}")
            print(f"   - 총 차시: {course_data['total_lessons']}")
            print(f"   - 챕터 수: {len(course_data['chapters'])}")
        print("✅ 파싱 완료")
        print()

        # 2. 생성
        generator = ContentGenerator(
            course_data=course_data,
            output_dir=args.output,
            template=args.template
        )

        generator.generate(dry_run=args.dry_run)

        if not args.dry_run:
            print()
            print("=" * 60)
            print(f"🎉 성공! {course_data['course_code']} 생성 완료")
            print(f"📂 위치: {Path(args.output) / course_data['course_code']}")
            print("=" * 60)

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
