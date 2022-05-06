# setup.py
from setuptools import setup, find_packages
setup(
    name='container_controller',
    version='1.0.1',
    author='ebsud89',
    author_email='ebsud89@gmail.com',
    description='FlaskServer Container Controller',
    packages=find_packages(),
    py_modules=['main'],
    install_requires=[
        'Click'
    ],
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
