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

  # 템플릿 지정
  python -m content_generator -i 25ctvibec.xlsx -t ct2022

  # 미리보기만 (실제 생성 안 함)
  python -m content_generator -i 25ctvibec.xlsx --dry-run
        '''
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='입력 파일 (엑셀 또는 CSV)'
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

    # 파일 존재 확인
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
        print(f"📖 파일 파싱 중: {input_path.name}")
        course_data = parse_course_file(str(input_path))

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
