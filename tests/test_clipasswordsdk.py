#!/usr/bin/env python3

from pyaim import CLIPasswordSDK

aimcp = CLIPasswordSDK('/opt/CARKaim/sdk/clipasswordsdk')
r = aimcp.GetPassword(appid='pyAIM', safe='D-AWS-AccessKeys', username='AnsibleAWSUser')
print(r)