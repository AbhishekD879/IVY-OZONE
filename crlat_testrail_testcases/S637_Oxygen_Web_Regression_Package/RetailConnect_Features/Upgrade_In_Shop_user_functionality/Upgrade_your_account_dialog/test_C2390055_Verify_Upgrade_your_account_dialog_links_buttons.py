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
class Test_C2390055_Verify_Upgrade_your_account_dialog_links_buttons(Common):
    """
    TR_ID: C2390055
    NAME: Verify 'Upgrade your account' dialog links/buttons
    DESCRIPTION: This test case verifies the behaviour of the SB app when an in-shop user taps 'No Thanks', Close button ('X'), 'Upgrade' on upgrade pop-up dialog
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: The way to open upgrade dialog:
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in as an in-shop user
    PRECONDITIONS: OR
    PRECONDITIONS: 1. Being logged in as an in-shop user select NO THANKS on the dialog after login
    PRECONDITIONS: 2. Open MY ACCOUNT menu
    PRECONDITIONS: 3. Select CONNECT
    PRECONDITIONS: 4. Select UPGRADE
    PRECONDITIONS: OR
    PRECONDITIONS: 1. Being logged in as an in-shop user select NO THANKS on the dialog after login
    PRECONDITIONS: 2.
    PRECONDITIONS: a) Select DEPOSIT from header
    PRECONDITIONS: b) Open MY ACCOUNT and select DEPOSIT
    PRECONDITIONS: c) Open MY ACCOUNT, select CASHIER and DEPOSIT
    PRECONDITIONS: d) Open MY ACCOUNT, select CASHIER and WITHDRAW
    PRECONDITIONS: e) Open CONNECT from header and tap "Upgrade your Connect account to bet online"
    """
    keep_browser_open = True

    def test_001_tap_close_button_x(self):
        """
        DESCRIPTION: Tap Close button ('X')
        EXPECTED: * The upgrade page is closed
        EXPECTED: * User is redirected to the main page
        """
        pass

    def test_002_perform_any_scenario_from_preconditions(self):
        """
        DESCRIPTION: Perform any scenario from preconditions
        EXPECTED: The upgrade page is opened
        """
        pass

    def test_003_tap_no_thanks_button(self):
        """
        DESCRIPTION: Tap 'No Thanks' button
        EXPECTED: * The upgrade page is closed
        EXPECTED: * User is redirected to the main page
        """
        pass

    def test_004_perform_any_scenario_from_preconditions(self):
        """
        DESCRIPTION: Perform any scenario from preconditions
        EXPECTED: The upgrade pop-up dialog is opened
        """
        pass

    def test_005_tap_upgrade_button(self):
        """
        DESCRIPTION: Tap 'Upgrade' button
        EXPECTED: User is redirected to UPGRADE NOW page with form similar to the registration form
        EXPECTED: ![](index.php?/attachments/get/39787)
        """
        pass

    def test_006_perform_any_scenario_from_preconditions(self):
        """
        DESCRIPTION: Perform any scenario from preconditions
        EXPECTED: The upgrade page is opened
        """
        pass

    def test_007_tap_somewhere_outside_the_dialog(self):
        """
        DESCRIPTION: Tap somewhere outside the dialog
        EXPECTED: Upgrade page is still opened
        """
        pass
