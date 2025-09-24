# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pyAIM is a Python 3 client library for CyberArk Application Access Manager that simplifies credential retrieval from CyberArk's Privileged Access Security (PAS) Core Solution. It provides two main access methods:

1. **CLIPasswordSDK** - Local Credential Provider method using CLIPasswordSDK executable
2. **CCPPasswordREST** - Centralized Credential Provider method using REST API calls

## Development Commands

### Package Management
- Install dependencies: `pip install -r requirements.txt` or `pipenv install`
- Install package in development mode: `pip install -e .`
- Build package: `python setup.py sdist bdist_wheel`
- Upload to PyPI: `twine upload dist/*`

### Testing
- Run CLI Password SDK test: `python tests/test_clipasswordsdk.py`
- Run CCP Password REST test: `python tests/test_ccppasswordrest.py`
- Test PyPI installation: `./tests/test_pypi.sh`
- Test pip installation: `./tests/test_pip.sh`

## Code Architecture

### Core Components

**pyaim/__init__.py** - Main module exposing CLIPasswordSDK and CCPPasswordREST classes

**pyaim/aimcp.py** - CLIPasswordSDK class for local credential provider interaction:
- Cross-platform support (Linux, macOS, Windows)
- Executes CLIPasswordSDK binary with subprocess
- Handles parameter formatting based on OS (- vs / separators)
- Supports dual accounts and virtual usernames
- Returns parsed credential data as dictionary

**pyaim/aimccp.py** - CCPPasswordREST class for REST API interaction:
- HTTPS connections using http.client
- SSL certificate verification with optional bypass (True/False/path to CA bundle)
- Client certificate authentication support
- Production mode health checking (v1.5.4+)
- Enhanced error handling for service diagnostics
- JSON response parsing

**pyaim/version.py** - Version information used by setup.py

### Key Parameters

Both classes support similar query parameters:
- `appid` (required) - Application ID for authentication
- `safe` (required) - Safe name containing the account
- `folder` - Folder path (default: root)
- `object` or `username` - Account identifier (one required)
- `address`, `database`, `policyid`, `reason` - Optional filters
- `dual_accounts` - Enable virtual username support

### Testing Infrastructure

- Basic functional tests in `/tests/` directory
- Certificate files for CCP testing (ccp-cert.pem, ccp-privkey.pem)
- Shell scripts for package installation testing

## Package Distribution

- Uses setuptools with setup.py configuration
- Version managed in separate version.py file
- Dependencies: urllib3 (main), twine (dev)
- Supports Python 3.8+
- Published to PyPI as 'pyaim'

## Development Notes

- Cross-platform compatibility is critical - test on Linux, macOS, Windows
- SSL certificate verification should be configurable but default to secure
- Error handling should provide clear messages for common issues (missing CLIPasswordSDK, network errors, authentication failures)
- Dual account support requires special VirtualUsername parameter handling

## Production Mode Implementation (v1.5.4+)

### Health Check Pattern

**Important**: The `check_service()` method uses "production mode" by default:
- Does NOT make API calls to CCP
- Validates local configuration only (base_uri, service_path, SSL context)
- Returns success without generating CCP logs

**For actual health checks**, use `GetPassword()` with a dedicated test account:
- Provides real service validation
- Generates legitimate, filterable logs with proper AppID
- Recommended pattern per customer requirements (Country Financial, June 2025)

### Background & Rationale

Customer feedback indicated that health check endpoints were generating excessive error logs in CCP with unusable data (blank AppID/query fields in CP logs). The SOAP endpoint (`/v1.1/aim.asmx`) was also deprecated.

**Changes in v1.5.4:**
1. Migrated from SOAP to REST API (`/api/Accounts`)
2. Implemented production mode: `check_service()` performs local validation only
3. Enhanced `GetPassword()` error messages for health check use cases
4. Added support for custom certificate paths (file or directory)

### Migration from Legacy check_service()

If upgrading from versions < 1.5.4 that relied on `check_service()` for actual health checks:

1. Replace `check_service()` calls with `GetPassword()` using test credentials
2. Set up dedicated health check AppID and safe
3. Configure monitoring to catch `ConnectionError` exceptions
4. Update alert filtering to use the health check AppID

### Health Check Setup

Recommended approach for production monitoring:

```python
# Create dedicated health check credentials in CCP:
# - Safe: health_check_safe
# - Account: health_check_account
# - AppID: monitoring_appid (with read-only access)

try:
    response = aimccp.GetPassword(
        appid='monitoring_appid',
        safe='health_check_safe',
        object='health_check_account'
    )
    # Service healthy
except ConnectionError as e:
    # Service down or unreachable - alert
except Exception as e:
    # Other errors (auth, permissions) - investigate
```

This approach:
- Uses real CCP functionality
- Generates legitimate audit logs
- Provides accurate service status
- Allows alert suppression based on AppID