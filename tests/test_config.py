import unittest
from pathlib import Path

import pyaim


class TestDevelopmentConfig(TestCase):
    def create_cfginstances(self):
        self.wincli = cfg.BaseConfig.WIN_CLIPASSWORDSDK
        self.nixcli = cfg.BaseConfig.NIX_CLIPASSWORDSDK

    def test_app_is_development(self):
        self.assertTrue(self.wincli is Path('C:/Windows/Program Files (x86)/CyberArk/ApplicationPasswordSdk/CLIPasswordSDK.exe'))
        self.assertTrue(self.nixcli is Path('/opt/carkaim/sdk/CLIPasswordSDK'))


class TestTestingConfig(TestCase):
    def create_cfginstances(self):
        self.wincli = cfg.BaseConfig.WIN_CLIPASSWORDSDK
        self.nixcli = cfg.BaseConfig.NIX_CLIPASSWORDSDK

    def test_app_is_testing(self):
        self.assertTrue(self.wincli is Path('C:/Windows/Program Files (x86)/CyberArk/ApplicationPasswordSdk/CLIPasswordSDK.exe'))
        self.assertTrue(self.nixcli is Path('/opt/carkaim/sdk/CLIPasswordSDK'))


class TestProductionConfig(TestCase):
    def create_cfginstances(self):
        self.wincli = cfg.BaseConfig.WIN_CLIPASSWORDSDK
        self.nixcli = cfg.BaseConfig.NIX_CLIPASSWORDSDK

    def test_app_is_production(self):
        self.assertTrue(self.wincli is Path('C:/Windows/Program Files (x86)/CyberArk/ApplicationPasswordSdk/CLIPasswordSDK.exe'))
        self.assertTrue(self.nixcli is Path('/opt/carkaim/sdk/CLIPasswordSDK'))


if __name__ == "__main__":
    unittest.main()