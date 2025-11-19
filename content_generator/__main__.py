"""
CLI 진입점
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

from .parser import parse_course_file, get_sheet_names
from .generator import ContentGenerator
from . import config


def _create_batch_log(input_file: str, output_dir: str, template: str, batch_results: list):
    """배치 작업 로그 생성 (레포지토리 폴더)"""
    # 레포지토리 루트 경로 찾기 (__file__의 상위)
    repo_root = Path(__file__).parent.parent
    history_dir = repo_root / 'history'
    history_dir.mkdir(parents=True, exist_ok=True)

    # 현재 날짜+시간으로 파일명 생성 (YYMMDD_HHMM.json)
    now = datetime.now()
    filename = now.strftime('%y%m%d_%H%M.json')  # 예: 251119_1007.json
    history_file = history_dir / filename

    # 배치 로그 데이터 (간략한 정보만)
    courses = []
    success_count = 0
    fail_count = 0

    for result in batch_results:
        if result['status'] == 'success':
            success_count += 1
            generator = result['generator']

            courses.append({
                "sheet_name": result['sheet_name'],
                "course_code": result['course_code'],
                "subject": generator.course_data['subject'],
                "status": "success",
                "total_lessons": generator.course_data['total_lessons'],
                "chapters": len(generator.course_data['chapters']),
                "output_dir": str(generator.course_dir),
                "lessons": [
                    {
                        "number": lesson['number'],
                        "title": lesson['title'],
                        "video_url": lesson['video_url'],
                        "has_download": bool(lesson['download_url'])
                    }
                    for lesson in generator.course_data['lessons']
                ]
            })
        else:
            fail_count += 1
            courses.append({
                "sheet_name": result['sheet_name'],
                "status": "failed",
                "error": result.get('error', 'Unknown error')
            })

    log_data = {
        "generated_at": now.isoformat(),
        "batch_type": "all_sheets",
        "input_file": input_file,
        "output_dir": output_dir,
        "template": template,
        "total_courses": len(batch_results),
        "success_count": success_count,
        "fail_count": fail_count,
        "courses": courses
    }

    # 파일 저장
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    history_file.chmod(0o644)
    print()
    print(f"📝 배치 작업 이력 저장: {history_file}")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='교육 콘텐츠 폴더 구조 자동 생성 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
사용 예시:
  # 엑셀 파일에서 생성
  python -m content_generator -i 25ctvibec.xlsx -o ~/projects/contents_it/subjects

  # 특정 시트 탭 선택 (시트 이름으로)
  python -m content_generator -i 25ctvibec.xlsx -s "25ctvibec"

  # 특정 시트 탭 선택 (인덱스로, 0부터 시작)
  python -m content_generator -i 25ctvibec.xlsx -s 1

  # 모든 시트 일괄 처리 (TTL 제외)
  python -m content_generator -i 25ctvibec.xlsx --all-sheets

  # 템플릿 지정
  python -m content_generator -i 25ctvibec.xlsx -t ct2022

  # 설정 저장 및 재사용
  python -m content_generator -i 25ctvibec.xlsx --save-config
  python -m content_generator --use-last

  # 미리보기만 (실제 생성 안 함)
  python -m content_generator -i 25ctvibec.xlsx --dry-run
        '''
    )

    parser.add_argument(
        '-i', '--input',
        required=False,
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

    parser.add_argument(
        '--save-config',
        action='store_true',
        help='현재 설정 저장 (입력 파일, 출력 경로, 템플릿)'
    )

    parser.add_argument(
        '--use-last',
        action='store_true',
        help='마지막 저장된 설정 사용'
    )

    parser.add_argument(
        '--all-sheets',
        action='store_true',
        help='엑셀 파일의 모든 시트 처리 (\'TTL\' 시트 제외)'
    )

    args = parser.parse_args()

    # 저장된 설정 사용
    if args.use_last:
        if not config.has_config():
            print("❌ 저장된 설정이 없습니다.")
            print("   먼저 --save-config 옵션으로 설정을 저장하세요.")
            sys.exit(1)

        saved_config = config.load_config()
        print("📂 저장된 설정 사용:")
        print(f"   - 입력: {saved_config['input']}")
        print(f"   - 출력: {saved_config['output']}")
        print(f"   - 템플릿: {saved_config['template']}")
        print()

        # 저장된 설정으로 덮어쓰기 (CLI 인자가 없을 경우만)
        if not args.input:
            args.input = saved_config['input']
        if args.output == './output':  # 기본값인 경우
            args.output = saved_config['output']
        if args.template == 'ct2022':  # 기본값인 경우
            args.template = saved_config['template']

    # 입력 파일 확인
    if not args.input:
        print("❌ 오류: 입력 파일이 지정되지 않았습니다.")
        print("   -i 옵션으로 입력 파일을 지정하거나, --use-last 옵션을 사용하세요.")
        sys.exit(1)

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

        # --all-sheets 옵션: 모든 시트 처리
        if args.all_sheets:

            # 모든 시트 이름 가져오기
            sheet_names = get_sheet_names(args.input)
            # 'TTL' 제외
            target_sheets = [name for name in sheet_names if name != 'TTL']

            if not target_sheets:
                print("❌ 처리할 시트가 없습니다. (TTL 제외)")
                sys.exit(1)

            print(f"📋 처리할 시트 목록 ({len(target_sheets)}개):")
            for sheet in target_sheets:
                print(f"   - {sheet}")
            print()

            # 각 시트마다 처리
            success_count = 0
            fail_count = 0
            batch_results = []  # 배치 처리 결과 저장

            for sheet in target_sheets:
                print("=" * 60)
                print(f"📄 시트 처리 중: {sheet}")
                print("=" * 60)

                try:
                    # 파싱
                    course_data = parse_course_file(args.input, sheet)

                    if args.verbose:
                        print(f"   - 과정 코드: {course_data['course_code']}")
                        print(f"   - 과정명: {course_data['subject']}")
                        print(f"   - 총 차시: {course_data['total_lessons']}")
                        print(f"   - 챕터 수: {len(course_data['chapters'])}")
                    print("✅ 파싱 완료")
                    print()

                    # 생성
                    generator = ContentGenerator(
                        course_data=course_data,
                        output_dir=args.output,
                        template=args.template,
                        input_file=args.input  # 실제 파일 경로 전달
                    )

                    generator.generate(dry_run=args.dry_run)

                    if not args.dry_run:
                        print(f"✅ {course_data['course_code']} 생성 완료")
                        print()
                        success_count += 1

                        # 배치 결과에 추가
                        batch_results.append({
                            "sheet_name": sheet,
                            "course_code": course_data['course_code'],
                            "status": "success",
                            "generator": generator
                        })

                except Exception as e:
                    print(f"❌ {sheet} 시트 처리 실패: {e}")
                    if args.verbose:
                        import traceback
                        traceback.print_exc()
                    print()
                    fail_count += 1

                    # 실패한 경우도 기록
                    batch_results.append({
                        "sheet_name": sheet,
                        "course_code": None,
                        "status": "failed",
                        "error": str(e)
                    })
                    continue

            # 최종 결과
            print("=" * 60)
            print(f"📊 전체 처리 결과")
            print(f"   - 성공: {success_count}개")
            print(f"   - 실패: {fail_count}개")
            print(f"   - 총: {len(target_sheets)}개")
            print("=" * 60)

            # 배치 작업 로그 생성
            if not args.dry_run and batch_results:
                _create_batch_log(args.input, args.output, args.template, batch_results)

        # 단일 시트 처리 (기존 로직)
        else:
            # 1. 파싱
            input_name = Path(args.input).name
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
                template=args.template,
                input_file=args.input
            )

            generator.generate(dry_run=args.dry_run)

            if not args.dry_run:
                print()
                print("=" * 60)
                print(f"🎉 성공! {course_data['course_code']} 생성 완료")
                print(f"📂 위치: {Path(args.output) / course_data['course_code']}")
                print("=" * 60)

                # 설정 저장
                if args.save_config:
                    print()
                    config.save_config(
                        input_file=args.input,
                        output_dir=args.output,
                        template=args.template
                    )
                    print()
                    print("💡 다음번에는 --use-last 옵션으로 간편하게 실행하세요:")
                    print(f"   python3 -m content_generator --use-last")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
