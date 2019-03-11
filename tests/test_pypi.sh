#!/bin/bash
#
# Upload Package to test.pypi.org

python3 -m pip install --upgrade setuptools wheel >/dev/null
python3 setup.py sdist bdist_wheel >/dev/null
python3 -m pip install --upgrade twine >/dev/null
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*