import os.path

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

PACKAGE_NAME = "pyaim"
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(CURRENT_DIR, PACKAGE_NAME, "version.py")

VERSION_DATA = {}
with open(VERSION_FILE, "r") as version_fp:
    exec(version_fp.read(), VERSION_DATA)

setuptools.setup(
    name="pyaim",
    version=VERSION_DATA['__version__'],
    author="Joe Garcia",
    author_email="joe.garcia@cyberark.com",
    description="CyberArk Application Access Manager Client Library for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/infamousjoeg/pyaim",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Office/Business",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    keywords=[
        "cyberark",
        "security",
        "vault",
        "aim",
        "aam",
        "privileged access",
        "identity",
        "pam",
        "pim",
        "pas"
        ],
    project_urls={
        'Bug Reports': 'https://github.com/infamousjoeg/pyaim/issues/new?assignees=&labels=&template=bug_report.md&title=',
        'Feature Requests': 'https://github.com/infamousjoeg/pyaim/issues/new?assignees=&labels=&template=feature_request.md&title=',
        'Source': 'https://github.com/infamousjoeg/pyaim'
    }
)
