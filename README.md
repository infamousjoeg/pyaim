# pyAIM<!-- omit from toc -->

![](assets/pyAIM-sm.png)

![GitHub last commit](https://img.shields.io/github/last-commit/infamousjoeg/pyaim.svg) [![GitHub issues](https://img.shields.io/github/issues/infamousjoeg/pyaim.svg?color=blue)](https://github.com/infamousjoeg/pyaim/issues) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyaim.svg) ![GitHub top language](https://img.shields.io/github/languages/top/infamousjoeg/pyaim.svg?color=yellow)  [![PyPI](https://img.shields.io/pypi/v/pyaim.svg)](https://pypi.org/project/pyaim) [![PyPI - Downloads](https://img.shields.io/pypi/dm/pyaim.svg?color=blue)](https://pypi.org/project/pyaim) [![Keybase PGP](https://img.shields.io/keybase/pgp/infamousjoeg.svg)](https://keybase.io/infamousjoeg) [![GitHub](https://img.shields.io/github/license/infamousjoeg/pyaim.svg?color=blue)](LICENSE)

> CyberArk Application Access Manager Client Library for Python 3

This project simplifies the interaction between a Python 3 application or script and CyberArk's Application Access Manager's Credential Provider using the appropriate CLIPasswordSDK executable for the Operating System being used.  By simplifying this process, developers are only required to change four (4) lines of code in their Python 3 applications and scripts to securely retrieve privileged secrets from CyberArk's Privileged Access Security (PAS) Core Solution as opposed to thirty or more (30+) without the use of this provided Client Library.

## Table of Contents <!-- omit from toc -->

- [Install](#install)
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
  - [Check AIMWebService Availability - check\_service()](#check-aimwebservice-availability---check_service)
    - [Centralized Credential Provider (CCPPasswordREST) Method](#centralized-credential-provider-ccppasswordrest-method-1)
  - [Retrieve Account - GetPassword()](#retrieve-account---getpassword)
    - [Credential Provider (CLIPasswordSDK) Method](#credential-provider-clipasswordsdk-method-1)
      - [Supported Parameters](#supported-parameters)
        - [Query Parameters](#query-parameters)
      - [Example](#example)
    - [Centralized Credential Provider (CCPPasswordREST) Method](#centralized-credential-provider-ccppasswordrest-method-2)
      - [Supported Parameters](#supported-parameters-1)
        - [CCPPasswordREST()](#ccppasswordrest)
        - [Query Parameters](#query-parameters-1)
      - [Example](#example-1)
      - [Example with Client Certificate Authentication](#example-with-client-certificate-authentication)
      - [Example with Custom Service Path](#example-with-custom-service-path)
- [Maintainer](#maintainer)
- [Contributing](#contributing)
- [License](#license)

## Install

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

### Check AIM Web Service - check_service()

⚠️ **Important**: In production mode (default), `check_service()` validates local configuration **without making API calls** to avoid generating CCP logs. For actual service health checks, use `GetPassword()` with test credentials.

#### Centralized Credential Provider (CCPPasswordREST) Method

**Configuration Validation (No API Call)**
```python
from pyaim import CCPPasswordREST

# Validates configuration locally without contacting CCP
aimccp = CCPPasswordREST('https://ccp.cyberarkdemo.example', verify=True)
config_status = aimccp.check_service()
print(config_status)
# Output: "Configuration validated for ccp.cyberarkdemo.example/AIMWebService. Use GetPassword() to verify service health."
```

**Production Health Check (Recommended)**
```python
from pyaim import CCPPasswordREST

aimccp = CCPPasswordREST('https://ccp.cyberarkdemo.example', verify=True)

# Health check using actual credential retrieval
try:
    response = aimccp.GetPassword(
        appid='monitoring_appid',
        safe='health_check_safe',
        object='health_check_account'
    )
    print("✓ CCP service is healthy and accessible")
    print(f"Retrieved account: {response.get('Username', 'N/A')}")
except ConnectionError as e:
    print(f"✗ CCP service unhealthy: {e}")
    # Handle service down/unreachable scenario
except ValueError as e:
    print(f"✗ Configuration error: {e}")
    # Handle parameter validation errors
except Exception as e:
    print(f"✗ CCP error: {e}")
    # Handle other errors
```

### Retrieve Account - GetPassword()

#### Credential Provider (CLIPasswordSDK) Method

##### Supported Parameters

###### Query Parameters

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
* output _(default: Password)_
* delimiter _(default: ,)_
* dual_accounts _(default: False)_

For compatibility with Dual Accounts where you are referencing a `VirtualUsername` - use the `username` parameter and ensure `dual_accounts=True`.

##### Example

```python
from pyaim import CLIPasswordSDK

aimcp = CLIPasswordSDK('/opt/CARKaim/sdk/clipasswordsdk')
response = aimcp.GetPassword(appid='appID',safe='safeName',object='objectName',output='PassProps.Username,Password',delimiter='|')

print('Full Response: {}'.format(response))
print('Username: {}'.format(response['PassProps.Username']))
print('Password: {}'.format(response['Password']))
```

#### Centralized Credential Provider (CCPPasswordREST) Method

##### Supported Parameters

###### CCPPasswordREST()

* url _(required)_
* verify _(default: True)_ - SSL certificate verification. Accepts:
  * `True` - Use system's default certificate bundle
  * `False` - Disable SSL verification (not recommended for production)
  * `/path/to/cert.pem` - Path to custom certificate bundle file
  * `/path/to/cert/dir` - Path to directory containing certificates (must be processed with c_rehash)
* cert _(default: None)_
* timeout _(default: 30)_

###### Query Parameters

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
* dual_accounts _(default: False)_

For compatibility with Dual Accounts where you are referencing a `VirtualUsername` - use the `username` parameter and ensure `dual_accounts=True`.

##### Example

```python
from pyaim import CCPPasswordREST

# set verify=False to ignore SSL
aimccp = CCPPasswordREST('https://ccp.cyberarkdemo.example', 'AIMWebService', verify=True, timeout=10)

service_status = aimccp.check_service()

if service_status == 'SUCCESS: AIMWebService Found. Status Code: 200':
    response = aimccp.GetPassword(appid='appid',safe='safe',object='objectName',reason='Reason message')
    print('Full Python Object: {}'.format(response))
    print('Username: {}'.format(response['Username']))
    print('Password: {}'.format(response['Content']))
else:
    raise Exception(service_status)
```

##### Example with Client Certificate Authentication

```python
from pyaim import CCPPasswordREST

# set verify=False to ignore SSL
aimccp = CCPPasswordREST('https://ccp.cyberarkdemo.example', verify=True, cert=('/path/to/cert.pem', '/path/to/key.pem'))

...
```

##### Example with Custom Service Path

```python
from pyaim import CCPPasswordREST

# set verify=False to ignore SSL
aimccp = CCPPasswordREST('https://ccp.cyberarkdemo.example', 'AIMWebServiceDEV', verify=True)

...
```

##### Example with Custom Certificate Bundle

```python
from pyaim import CCPPasswordREST

# Use custom certificate bundle for SSL verification
aimccp = CCPPasswordREST('https://ccp.cyberarkdemo.example', verify='/path/to/custom-ca-bundle.pem')

# Or use a directory of certificates
aimccp = CCPPasswordREST('https://ccp.cyberarkdemo.example', verify='/etc/ssl/certs')

# Validate configuration
config_status = aimccp.check_service()
print(config_status)

# Actual credential retrieval
response = aimccp.GetPassword(appid='appid',safe='safe',object='objectName',reason='Reason message')
print('Username: {}'.format(response['Username']))
print('Password: {}'.format(response['Content']))
```

## Health Check Best Practices

### Why GetPassword() for Health Checks?

The `GetPassword()` method is the recommended approach for health checking because:

1. **No False Logs**: Doesn't generate error logs in CCP with blank AppID/query fields
2. **Real Validation**: Actually tests the full authentication and retrieval flow
3. **Production Ready**: Uses legitimate credentials, avoiding synthetic health check calls
4. **Actionable Errors**: Provides specific error messages for troubleshooting

### Setting Up Health Check Accounts

Create a dedicated account in CCP for health monitoring:

1. Create a safe called `health_check_safe` (or similar)
2. Store a test account called `health_check_account` with a known password
3. Create an AppID called `monitoring_appid` with read-only access to the safe
4. Use these credentials in your health check scripts

**Benefits of this approach:**
- Uses real CCP functionality
- Generates legitimate, filterable audit logs
- Provides accurate service status
- Allows alert suppression based on AppID if needed

### Migration from Legacy check_service()

If upgrading from versions < 1.5.4 that relied on `check_service()` for actual health checks:

1. Replace `check_service()` calls with `GetPassword()` using test credentials
2. Set up dedicated health check AppID and safe (see above)
3. Configure monitoring to catch `ConnectionError` exceptions for service down alerts
4. Update alert filtering to use the new health check AppID instead of generic error patterns

## Maintainer

[@infamousjoeg](https://github.com/infamousjoeg)

[buymeacoffee]: https://www.buymeacoffee.com/infamousjoeg
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png

## Contributing

Contributions are open!  Check out [CONTRIBUTING.md]() for more details!

## License

[MIT](LICENSE)
