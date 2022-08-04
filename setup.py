""" Setup file for module """
from setuptools import setup

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

with open('requirements.txt', encoding='utf8') as f:
    requirements = f.readlines()

setup(
    name='tgfp-lib',
    version='1.1.1',
    packages=['tgfp_lib'],
    python_requires='>=3.10.*',
    url='https://github.com/johnsturgeon/tgfp-lib',
    license='MIT',
    author='John Sturgeon',
    author_email='john.sturgeon@me.com',
    install_requires=requirements,
    description='Python library for The Great Football Pool',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
