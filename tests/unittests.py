import unittest     # AAA Model: Arrange, Act, Assert
                    # # Arrange:    Setting up of all the pre-reqs required for the test to run
                    # # Act:        Run the actual code under test
                    # # Assert:     Verify whether the code is indeed running as expected
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from pyaim import CCPPasswordREST, CLIPasswordSDK

class TestCCPPasswordREST(unittest.TestCase):

    def test_ccppasswordrest_webservice_found(self):
        aimccp = CCPPasswordREST('https://cyberark.joegarcia.dev')
        service_status = aimccp.check_service()
        if service_status == 'SUCCESS: AIMWebService Found. Status Code: 200':
            self.assertTrue(True)
        else:
            self.assertTrue(False)


    def test_ccppasswordrest_acctobj_found(self):
        aimccp = CCPPasswordREST('https://cyberark.joegarcia.dev')
        service_status = aimccp.check_service()
        if service_status == 'SUCCESS: AIMWebService Found. Status Code: 200':
            account_object = aimccp.GetPassword(appid='pyAIM', safe='DemoSafe', object='RESTAPI-DemoUser', reason="pyAIM Unit Testing")
        else:
            self.assertTrue(False)

        self.assertEqual(account_object['UserName'], 'DemoUser')
        self.assertEqual(account_object['Address'], '10.0.4.48')
        self.assertEqual(account_object['DeviceType'], 'Operating System')
        self.assertEqual(account_object['PolicyID'], 'WinDomain')
        self.assertEqual(account_object['LogonDomain'], 'JOEGARCIA')


class TESTCLIPasswordSDK(unittest.TestCase):

    def test_clipasswordsdk_config(self):
        pass


    def test_clipasswordsdk_acctobj(self):
        pass


if __name__ == "__main__":
    unittest.main()