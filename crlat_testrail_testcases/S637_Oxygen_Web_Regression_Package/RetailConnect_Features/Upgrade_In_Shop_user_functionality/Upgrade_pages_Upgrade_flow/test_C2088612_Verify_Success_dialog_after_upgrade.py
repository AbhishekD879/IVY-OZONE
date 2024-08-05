import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2088612_Verify_Success_dialog_after_upgrade(Common):
    """
    TR_ID: C2088612
    NAME: Verify 'Success' dialog after upgrade
    DESCRIPTION: This test case verifies Success message after user has been upgraded to multi-channel
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in with in-shop user
    """
    keep_browser_open = True

    def test_001_click_the_upgrade_button_on_upgrade_dialog(self):
        """
        DESCRIPTION: Click the **UPGRADE** button on Upgrade dialog
        EXPECTED: A user is redirected to the 'registration' screen
        """
        pass

    def test_002_provide_all_necessary_data(self):
        """
        DESCRIPTION: Provide all necessary data
        EXPECTED: All possible fields are prepopulated with data from the system
        """
        pass

    def test_003_click_the_create_account_button(self):
        """
        DESCRIPTION: Click the **Create Account** button
        EXPECTED: User is logged out from the app and redirected to the login page with a message:
        EXPECTED: "You have upgraded your account. Please use your Username and Password to log in with."
        """
        pass
