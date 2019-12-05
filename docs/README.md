# pyAIM <!-- OMIT IN TOC -->

![](assets/pyAIM-sm.png)

![GitHub last commit](https://img.shields.io/github/last-commit/infamousjoeg/pyaim.svg) [![GitHub issues](https://img.shields.io/github/issues/infamousjoeg/pyaim.svg?color=blue)](https://github.com/infamousjoeg/pyaim/issues) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyaim.svg) ![GitHub top language](https://img.shields.io/github/languages/top/infamousjoeg/pyaim.svg?color=yellow)  [![PyPI](https://img.shields.io/pypi/v/pyaim.svg)](https://pypi.org/project/pyaim) [![PyPI - Downloads](https://img.shields.io/pypi/dm/pyaim.svg?color=blue)](https://pypi.org/project/pyaim) [![Keybase PGP](https://img.shields.io/keybase/pgp/infamousjoeg.svg)](https://keybase.io/infamousjoeg) [![GitHub](https://img.shields.io/github/license/infamousjoeg/pyaim.svg?color=blue)](LICENSE)

> CyberArk Application Access Manager Client Library for Python 3

This project simplifies the interaction between a Python 3 application or script and CyberArk's Application Access Manager's Credential Provider using the appropriate CLIPasswordSDK executable for the Operating System being used.  By simplifying this process, developers are only required to change four (4) lines of code in their Python 3 applications and scripts to securely retrieve privileged secrets from CyberArk's Privileged Access Security (PAS) Core Solution as opposed to thirty or more (30+) without the use of this provided Client Library.

### New in Version 1.2.0: <!-- OMIT IN TOC -->

Added support for all possible parameters for both AAM Credential Provider (CLIPasswordSDK) and AAM Central Credential Provider (CCPPasswordREST).

## Table of Contents <!-- OMIT IN TOC -->

- [pyAIM](#pyaim)
    - [New in Version 1.2.0: ](#new-in-version-120)
  - [Table of Contents ](#table-of-contents)
  - [Install](#install)
    - [Pre-Requisite](#pre-requisite)
      - [Credential Provider (CLIPasswordSDK) Method](#credential-provider-clipasswordsdk-method)
      - [Centralized Credential Provider (CCPPasswordREST) Method](#centralized-credential-provider-ccppasswordrest-method)
    - [Windows](#windows)
      - [Install Latest Python 3](#install-latest-python-3)
      - [Install pyAIM via Pip](#install-pyaim-via-pip)
    - [Linux](#linux)
      - [Ubuntu/Debian](#ubuntudebian)
        - [Install Latest Python 3](#install-latest-python-3-1)
        - [Install pyAIM via Pip](#install-pyaim-via-pip-1)
      - [RHEL/CentOS](#rhelcentos)
        - [Install Latest Python 3](#install-latest-python-3-2)
          - [RHEL](#rhel)
          - [CentOS](#centos)
        - [Install pyAIM via Pip](#install-pyaim-via-pip-2)
    - [MacOS](#macos)
    - [Z/OS](#zos)
      - [Install Latest Python 3](#install-latest-python-3-3)
      - [Install pyAIM via Pip](#install-pyaim-via-pip-3)
  - [Usage](#usage)
    - [Check AIMWebService Availability - check_service()](#check-aimwebservice-availability---check_service)
      - [Centralized Credential Provider (CCPPasswordREST) Method](#centralized-credential-provider-ccppasswordrest-method-1)
    - [Retrieve Account - GetPassword()](#retrieve-account---getpassword)
      - [Credential Provider (CLIPasswordSDK) Method](#credential-provider-clipasswordsdk-method-1)
        - [Supported Parameters](#supported-parameters)
        - [Example](#example)
      - [Centralized Credential Provider (CCPPasswordREST) Method](#centralized-credential-provider-ccppasswordrest-method-2)
        - [Supported Parameters](#supported-parameters-1)
        - [Example](#example-1)
  - [Maintainer](#maintainer)
  - [Contributing](#contributing)
  - [License](#license)

## Install

### Pre-Requisite

#### Credential Provider (CLIPasswordSDK) Method

* CyberArk Application Access Manager Credential Provider installed locally.

#### Centralized Credential Provider (CCPPasswordREST) Method

* CyberArk Application Access Manager Centralized Credential Provider and AIMWebService

For information on how to install either of these providers, please refer to CyberArk's Application Access Manager Installation Guide or reach out to your assigned Customer Success Technical Advisor.

### Windows

#### Install Latest Python 3

[Install the Python 3 release for Windows](https://www.python.org/downloads/windows/)

#### Install pyAIM via Pip

`> pip3 install pyaim`

### Linux

#### Ubuntu/Debian

##### Install Latest Python 3

`$ sudo apt install -y python3 python3-pip`

##### Install pyAIM via Pip

`$ pip3 install pyaim`

#### RHEL/CentOS

##### Install Latest Python 3

###### RHEL

Follow the [EPEL Documentation](https://fedoraproject.org/wiki/EPEL#How_can_I_use_these_extra_packages.3F) to ensure you have the EPEL Release repository available.

`$ sudo yum install -y https://rhel7.iuscommunity.org/ius-release.rpm`

`$ sudo yum update`

`$ sudo yum install -y python36u python36u-libs python36u-devel python36u-pip`

###### CentOS

`$ sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm`

`$ sudo yum update`

`$ sudo yum install -y python36u python36u-libs python36u-devel python36u-pip`

##### Install pyAIM via Pip

`$ pip3 install pyaim`

### MacOS

No support provided yet.

### Z/OS

pyAIM is untested on Z/OS but should work in theory.

#### Install Latest Python 3

Rocket Software has [ported Python 2 and 3](https://www.rocketsoftware.com/zos-open-source) for Z/OS

#### Install pyAIM via Pip

`$ pip3 install pyaim`

## Usage

### Check AIMWebService Availability - check_service()

#### Centralized Credential Provider (CCPPasswordREST) Method

```python
from pyaim import CCPPasswordREST

aimccp = CCPPasswordREST('https://ccp.cyberarkdemo.example', verify=True) # set verify=False to ignore SSL
service_status = aimccp.check_service()
print(service_status)
```

### Retrieve Account - GetPassword()

#### Credential Provider (CLIPasswordSDK) Method

##### Supported Parameters

* appid _(required)_
* safe _(required)_
* folder _(default: root)_
* object _(this or `username` required)_
* username _(this or `object` required)_
* address
* database
* policyid
* reason
* query_format _(default: 1)_
* connport
* sendhash _(default: False)_

For compatibility with Dual Accounts where you are refercing a `VirtualUsername` - use the `username` parameter.

##### Example

```python
from pyaim import CLIPasswordSDK

aimcp = CLIPasswordSDK('/opt/CARKaim/sdk/clipasswordsdk')
response = aimcp.GetPassword(appid='appID',safe='safeName',objectName='objectName',output='PassProps.Username,Password')

print('Full Response: {}'.format(response))
print('Username: {}'.format(response['PassProps.Username']))
print('Password: {}'.format(response['Password']))
```

#### Centralized Credential Provider (CCPPasswordREST) Method

##### Supported Parameters

* appid _(required)_
* safe _(required)_
* folder _(default: root)_
* object _(this or `username` required)_
* username _(this or `object` required)_
* address
* database
* policyid
* reason
* query_format _(default: exact)_

For compatibility with Dual Accounts where you are refercing a `VirtualUsername` - use the `username` parameter.

##### Example

```python
from pyaim import CCPPasswordREST

aimccp = CCPPasswordREST('https://ccp.cyberarkdemo.example', verify=True) # set verify=False to ignore SSL

service_status = aimccp.check_service()

if service_status == 'SUCCESS: AIMWebService Found. Status Code: 200':
    response = aimccp.GetPassword(appid='appid',safe='safe',object='objectName',reason='Reason message')
    print('Full Python Object: {}'.format(response))
    print('Username: {}'.format(response['Username']))
    print('Password: {}'.format(response['Content']))
else:
    raise Exception(service_status)
```

## Maintainer

[@infamousjoeg](https://github.com/infamousjoeg)

## Contributing

For the time being, only internal CyberArk contributions are being considered.

Feel free to report any feature requests or bugs on the [GitHub Issues](https://github.com/infamousjoeg/pyaim/issues) page.

Keep checking back for an update regarding open Contributions in the near future.

## License

[MIT](LICENSE) © Joe Garcia, CISSP
