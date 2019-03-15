# pyAIM <!-- OMIT IN TOC -->

![GitHub last commit](https://img.shields.io/github/last-commit/infamousjoeg/pyaim.svg) [![GitHub issues](https://img.shields.io/github/issues/infamousjoeg/pyaim.svg?color=blue)](https://github.com/infamousjoeg/pyaim/issues) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyaim.svg) ![GitHub top language](https://img.shields.io/github/languages/top/infamousjoeg/pyaim.svg?color=yellow)  [![PyPI](https://img.shields.io/pypi/v/pyaim.svg)](https://pypi.org/projects/pyaim) [![PyPI - Downloads](https://img.shields.io/pypi/dm/pyaim.svg?color=blue)](https://pypi.org/projects/pyaim) [![Keybase PGP](https://img.shields.io/keybase/pgp/infamousjoeg.svg)](https://keybase.io/infamousjoeg) [![GitHub](https://img.shields.io/github/license/infamousjoeg/pyaim.svg?color=blue)](LICENSE)

> CyberArk Application Access Manager Client Library for Python 3

This project simplifies the interaction between a Python 3 application or script and CyberArk's Application Access Manager's Credential Provider using the appropriate CLIPasswordSDK executable for the Operating System being used.  By simplifying this process, developers are only required to change four (4) lines of code in their Python 3 applications and scripts to securely retrieve privileged secrets from CyberArk's Privileged Access Security (PAS) Core Solution as opposed to thirty or more (30+) without the use of this provided Client Library.

## Table of Contents <!-- OMIT IN TOC -->

- [Install](#install)
  - [Windows](#windows)
  - [Linux](#linux)
    - [Ubuntu/Debian](#ubuntudebian)
      - [Install Latest Python 3](#install-latest-python-3)
      - [Install pyAIM via Pip](#install-pyaim-via-pip)
    - [RHEL/CentOS](#rhelcentos)
      - [Enable epel-release if using RHEL](#enable-epel-release-if-using-rhel)
      - [Install Latest Python 3](#install-latest-python-3-1)
        - [RHEL](#rhel)
        - [CentOS](#centos)
      - [Install pyAIM via Pip](#install-pyaim-via-pip-1)
  - [MacOS](#macos)
  - [Z/OS](#zos)
- [Usage](#usage)
  - [Retrieve Account](#retrieve-account)
    - [Credential Provider (CLIPasswordSDK) Method](#credential-provider-clipasswordsdk-method)
- [Maintainer](#maintainer)
- [Contributing](#contributing)
- [License](#license)

## Install

### Windows

[Install the Python 3 release for Windows](https://www.python.org/downloads/windows/)

`pip3 install pyaim`

### Linux

#### Ubuntu/Debian

##### Install Latest Python 3

`sudo apt install -y python3 python3-pip`

##### Install pyAIM via Pip

`pip3 install pyaim`

#### RHEL/CentOS

##### Enable epel-release if using RHEL

Follow the [EPEL Documentation](https://fedoraproject.org/wiki/EPEL#How_can_I_use_these_extra_packages.3F).

##### Install Latest Python 3

###### RHEL

`sudo yum install -y https://rhel7.iuscommunity.org/ius-release.rpm`
`sudo yum update`
`sudo yum install -y python36u python36u-libs python36u-devel python36u-pip`

###### CentOS

`sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm`
`sudo yum update`
`sudo yum install -y python36u python36u-libs python36u-devel python36u-pip`

##### Install pyAIM via Pip

`pip install pyaim`

### MacOS

No support provided yet.

### Z/OS

No support provided yet.

## Usage

### Retrieve Account

#### Credential Provider (CLIPasswordSDK) Method

```python
from pyaim import CLIPasswordSDK

aimcp = CLIPasswordSDK('/opt/CARKaim/sdk/clipasswordsdk')
response = aimcp.GetPassword('appID','safeName','objectName')

print('Full Response: {}'.format(response))
print('Username: {}'.format(response['Username']))
print('Password: {}'.format(response['Password']))
print('Address: {}'.format(response['Address']))
print('Port: {}'.format(response['Port']))
print('PasswordChangeInProcess: {}'.format(response['PasswordChangeInProcess']))
```

## Maintainer

[@infamousjoeg](https://github.com/infamousjoeg)

## Contributing

For the time being, only internal CyberArk contributions are being considered.

Feel free to report any feature requests or bugs on the [GitHub Issues](https://github.com/infamousjoeg/pyaim/issues) page.

Keep checking back for an update regarding open Contributions in the near future.

## License

[MIT](LICENSE) © Joe Garcia, CISSP