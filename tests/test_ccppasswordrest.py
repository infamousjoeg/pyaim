#!/usr/bin/env python3

from pyaim import CCPPasswordREST

aimccp = CCPPasswordREST('https://cyberark.joegarcia.dev/')
r = aimccp.GetPassword(appid='pyAIM',safe='D-AWS-AccessKeys',username='AnsibleAWSUser')
print(r)