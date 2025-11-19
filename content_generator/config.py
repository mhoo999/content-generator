"""
설정 파일 관리 모듈
"""

import json
from pathlib import Path
from typing import Dict, Optional


CONFIG_DIR = Path.home() / '.content-generator'
CONFIG_FILE = CONFIG_DIR / 'config.json'


def save_config(input_file: str, output_dir: str, template: str = "ct2022"):
    """
    설정 저장

    Args:
        input_file: 입력 파일 경로
        output_dir: 출력 디렉토리
        template: 템플릿 종류
    """
    config = {
        "input": input_file,
        "output": output_dir,
        "template": template
    }

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"✅ 설정 저장 완료: {CONFIG_FILE}")
    print(f"   - 입력 파일: {input_file}")
    print(f"   - 출력 경로: {output_dir}")
    print(f"   - 템플릿: {template}")


def load_config() -> Optional[Dict]:
    """
    설정 불러오기

    Returns:
        저장된 설정 (없으면 None)
    """
    if not CONFIG_FILE.exists():
        return None

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    return config


def has_config() -> bool:
    """설정 파일 존재 여부"""
    return CONFIG_FILE.exists()
