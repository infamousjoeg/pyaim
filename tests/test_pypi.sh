#!/bin/bash
#
# Upload Package to test.pypi.org

echo "Running sdist and bdist_wheel from setup.py..."
python3 setup.py sdist bdist_wheel
echo "Uploading to test.pypi.org via Twine..."
twine upload --repository-url https://test.pypi.org/legacy/ dist/*