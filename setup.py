# setup.py
from setuptools import setup, find_packages

# setup(
#     name='dcc',
#     version='1.0.0',
#     author='ebsud89',
#     author_email='ebsud89@1thefull.com',
#     description='Data Teams CMD for docker container control',
#     packages=find_packages(),
#     entry_points={
#         "console_scripts": [
#             "container-controller = container-controller.main:main"
#             #            "dcc = container-controller.main:main"
#         ]
#     },
#     classifiers=[
#         'Programming Language :: Python :: 3',
#         'License :: OSI Approved :: MIT License',
#         'Operating System :: OS Independent',
#     ],
# )

setup(
    # 모듈명
    name='container_controller',
    # 버전
    version='1.0.0',
    author='SJQuant',
    author_email='seonujang92@gmail.com',
    description='Greet someone',
    packages=find_packages(),
    # 여기가 중요합니다.
    entry_points={
        "console_scripts": [
            # hello라는 명령어를 실행하면
            # hello모듈 main.py에서 main함수를 실행한다는 의미입니다.
            # "hello = hello.main:main"
            "container_controller = container_controller.main:main"
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
