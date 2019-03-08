#!/bin/bash
#
# Upload Package to test.pypi.org

python3 -m pip install --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install --upgrade twine
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*