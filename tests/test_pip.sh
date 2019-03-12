#!/bin/bash

pip3 uninstall -y pyaim
rm -rf ~/.cache/pip
pip3 install -i https://test.pypi.org/simple pyaim