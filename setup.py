from setuptools import setup, find_packages

setup(
    name='content-generator',
    version='1.0.0',
    description='교육 콘텐츠 폴더 구조 자동 생성 도구',
    author='메가존 IT 교육팀',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.0.0',
        'openpyxl>=3.1.0',
    ],
    entry_points={
        'console_scripts': [
            'content-generator=content_generator.__main__:main',
        ],
    },
    python_requires='>=3.7',
)
