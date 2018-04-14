from setuptools import setup

setup(
    name='archiver',
    version='1.0',
    packages=['archiver'],
    install_requires=['Click', 'pycryptodome'],
    entry_points='''
        [console_scripts]
        arc=archiver.main:archiver
    ''',
)
