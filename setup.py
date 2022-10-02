# coding: utf8

# import toml
from pip._internal.req import parse_requirements
from setuptools import setup

# TODO: Update version whenever changes
VERSION = '0.0.1.5'


def get_install_requirements():
    install_reqs = parse_requirements('requirements.txt', session='hack')
    return install_reqs


setup(
    # TODO: Change your library name and additional information down here
    name='py_header_lib',
    packages=[
        'py_header_lib',
        'py_header_lib.securities',
        'py_header_lib.grpc_services',
        'py_header_lib.grpc_services.common',
        'py_header_lib.grpc_services.common.proto',
    ],
    url='',
    download_url='',
    license='MIT',
    author='Đào Công Tuấn',
    author_email='tuandao864@gmail.com',
    description='The lib for Python modules.',
    install_requires=[
        'urllib3>=1.15',
        'environs>=4.2.0',
        'python-json-logger>=0.1.11',
        'pytest',
        'loguru>=0.5.3',
        'pytz>=2021.1',
        'pycryptodome>=3.10.1',
        'pyopenssl>=19.1.0',
        'inflection>=0.5.1',
        'arrow>=1.1.0',
    ],
    version=VERSION,

    # TODO (Optional): Set your entry-points (CLI apps to register) here
    entry_points={
        'console_scripts': ['py_header_lib=py_header_lib:env'],
    },

    # TODO: Choose your classifiers carefully
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
