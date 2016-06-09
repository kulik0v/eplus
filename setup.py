# -*- encoding: UTF-8 -*-

import os
from setuptools import setup, find_packages



# here = path.abspath(path.dirname(__file__))
# with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#     long_description = f.read()


setup(
    name='eplus',
    version='1.0.0',
    description='Google App Engine extensions',
    # long_description=long_description,
    url='https://github.com/kulik0v/eplus',
    download_url='https://github.com/kulik0v/eplus/archive/master.zip',
    author='WIX',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable

    # packages=find_packages(),
    packages=['eplus'],
    # install_requires=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'app_shell=eplus.console_shell:main',
        ],
    },
)

# pip install -e .
# pip install --user --upgrade .

