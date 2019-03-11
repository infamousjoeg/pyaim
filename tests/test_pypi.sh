#!/bin/bash
#
# Upload Package to test.pypi.org

echo "Upgrading setuptools and wheel..."
python3 -m pip install --upgrade setuptools wheel >/dev/null
echo "Running sdist and bdist_wheel from setup.py..."
python3 setup.py sdist bdist_wheel >/dev/null
echo "Upgrading Twine..."
python3 -m pip install --upgrade twine >/dev/null
echo "Uploading to test.pypi.org via Twine..."
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*