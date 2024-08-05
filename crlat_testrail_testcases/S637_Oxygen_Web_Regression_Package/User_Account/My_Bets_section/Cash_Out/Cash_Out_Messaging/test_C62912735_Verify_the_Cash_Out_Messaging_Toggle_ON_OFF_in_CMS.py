import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C62912735_Verify_the_Cash_Out_Messaging_Toggle_ON_OFF_in_CMS(Common):
    """
    TR_ID: C62912735
    NAME: Verify the Cash Out Messaging Toggle ON/OFF in CMS
    DESCRIPTION: This test case verifies the CMS configurations for Cash Out Messaging
    PRECONDITIONS: * User have CMS admin access
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be logged in to CMS
        """
        pass

    def test_002_navigate_to_system_configuration(self):
        """
        DESCRIPTION: Navigate to System Configuration
        EXPECTED: Disable the toggle
        """
        pass

    def test_003_validate_the_cash_out_messaging_in_fe(self):
        """
        DESCRIPTION: Validate the Cash Out Messaging in FE
        EXPECTED: * User should not see any Cash Out Messaging
        """
        pass

    def test_004_navigate_to_system_configuration(self):
        """
        DESCRIPTION: Navigate to System Configuration
        EXPECTED: Enable the toggle
        """
        pass

    def test_005_validate_the_cash_out_messaging_in_fe(self):
        """
        DESCRIPTION: Validate the Cash Out Messaging in FE
        EXPECTED: * Cash Out Messaging should be displayed as configured
        """
        pass
