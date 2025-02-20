import codecs
import os

from setuptools import setup, find_packages

def read(*parts):
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

long_description = read('README.md')

setup(
    name='twodo',
    version='0.0.1',
    description='CLI tool to manage twodo (todo) lists!',
    long_description=long_description,
    keywords='todo list task productivity project-management',
    author='Francois Chalifour, definitelyzoey',
    author_email='francois.chalifour@gmail.com, definitelyzo4y@gmail.com',
    url='https://github.com/francoischalifour/todo-cli and https://github.com/definitelyzoey/twodo',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'twodo=todo:main',
            'todo=todo:main'
        ]
    }
)
