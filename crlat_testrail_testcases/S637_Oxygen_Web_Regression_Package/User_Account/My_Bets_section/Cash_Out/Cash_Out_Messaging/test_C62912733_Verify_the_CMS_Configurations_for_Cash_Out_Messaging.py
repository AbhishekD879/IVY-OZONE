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
class Test_C62912733_Verify_the_CMS_Configurations_for_Cash_Out_Messaging(Common):
    """
    TR_ID: C62912733
    NAME: Verify the CMS Configurations for Cash Out Messaging
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
        EXPECTED: Add the Cash Out Messaging and SAVE
        """
        pass
