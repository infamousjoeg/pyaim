from pathlib import Path


class BaseConfig:
    """ Base Configuration """
    WIN_CLIPASSWORDSDK = Path('C:/Windows/Program Files (x86)/CyberArk/ApplicationPasswordSdk/CLIPasswordSDK.exe')
    NIX_CLIPASSWORDSDK = Path('/opt/carkaim/sdk/CLIPasswordSDK')


"""
Use the following classes to update CLIPasswordSDK location
based on environment.
"""

class DevelopmentConfig(BaseConfig):
    """ Development Configuration """
    pass


class TestingConfig(BaseConfig):
    """ Testing Configuration """
    pass


class ProductionConfig(BaseConfig):
    """ Production Configuration """
    pass