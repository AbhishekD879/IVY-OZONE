import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C352447_Verify_OXsoftSerial_and_OXuuid_parameters_setting_in_local_storage(Common):
    """
    TR_ID: C352447
    NAME: Verify 'OX.softSerial' and 'OX.uuid' parameters setting in local storage
    DESCRIPTION: This test case verifies 'OX.softSerial' and 'OX.uuid' parameters setting in local storage
    PRECONDITIONS: 1. To check local storage open dev tools -> select Application tab -> local storage section
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log in' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_003_check_remember_me_option_and_tap_log_in_button(self):
        """
        DESCRIPTION: Check 'Remember me' option and tap 'Log in' button
        EXPECTED: User is successfully logged in with permanet session
        """
        pass

    def test_004_verify_oxsoftserial_parameter_correctness_in_local_storage(self):
        """
        DESCRIPTION: Verify 'OX.softSerial' parameter correctness in local storage
        EXPECTED: 'OX.softSerial' parameter corresponds to 'softSerail' value from object
        """
        pass

    def test_005_verify_oxuuid_parameter_correctness_in_local_storage(self):
        """
        DESCRIPTION: Verify 'OX.uuid' parameter correctness in local storage
        EXPECTED: 'OX.uuid' parameter corresponds to 'deviceID' value from object
        """
        pass
