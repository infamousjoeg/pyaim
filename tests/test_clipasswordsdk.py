import unittest

import pyaim

class TestCLIPasswordSDK(BaseTestCase):
    def GetPassword(self):
        appid = "pyaim-test"
        safe = "TEST-RESTAPI"
        obj = "TEST-RESTAPI-uadmin"

        aimresp = pyaim.GetPassword(appid,safe,obj)

        self.assertFalse('APPAP282E' is in aimresp)
        self.assertTrue(aimresp is not None)


if __name__ == "__main__":
    unittest.main()