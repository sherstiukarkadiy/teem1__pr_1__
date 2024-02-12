from setuptools import setup, find_packages

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='subordinate_project_1',
    version='0.0.10',
    description='wery useful bot',
    long_description = long_description,
    url='http://github.com/dummy_user/useful',
    author='subordinate',
    author_email='',
    license='MIT',
    packages= find_packages(where='src'),
    package_dir= {'':'src'},
    install_requires = ['prompt_toolkit'],
    python_requires = '>=3',
    include_package_data=True,
    entry_points = {'console_scripts': ['subordinate = subordinate:main_func']}
    )
