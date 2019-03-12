#!/usr/bin/env python3

from pyaim import clipasswordsdk

aimcp = clipasswordsdk('/opt/CARKaim/sdk/clipasswordsdk')
r = aimcp.GetPassword('pyAIM','TEST-PYAIM','test-pyaim-uadmin')
print(r)