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
class Test_C2807970_Verify_navigation_to_from_Reactivation_page(Common):
    """
    TR_ID: C2807970
    NAME: Verify navigation to/from Reactivation page
    DESCRIPTION: This test case verifies navigation to Reactivation page
    DESCRIPTION: AUTOTEST [C9240768]
    PRECONDITIONS: * User's Account is closed (Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: Tap/click 'I want to close my Account' link within 'Account Closure' section)
    PRECONDITIONS: * Player Tag 'Account_Closed_By_Player' is set to 'True' in IMS
    PRECONDITIONS: * Player Tag 'On_login_Account_Closed_Message' is set in IMS
    PRECONDITIONS: * 'Reactivation' Log in message is created with the tag 'On_login_Account_Closed_Message' in IMS
    PRECONDITIONS: * The login pop up is set within IMS - configuration instructions can be found here https://drive.google.com/drive/u/2/folders/1pkGIbDBUp2rU_iWXh1ve18W0mwK71VMU
    PRECONDITIONS: * Log in
    PRECONDITIONS: * ''Reactivation' login pop up is displayed
    PRECONDITIONS: The user menu Reactivation item design: https://app.zeplin.io/project/5afd4876e6c84b4322fe1516/screen/5ba909141ca4575f402def38
    """
    keep_browser_open = True

    def test_001_clicktap_reactivation_url_within_on_login_pop_up(self):
        """
        DESCRIPTION: Click/tap 'Reactivation' url within on login pop up
        EXPECTED: User is redirected to Reactivation page within app
        """
        pass

    def test_002_clicktap_back_button(self):
        """
        DESCRIPTION: Click/tap 'Back' button
        EXPECTED: User is redirected to Home page
        """
        pass

    def test_003_log_out_and_log_in_with_the_same_user(self):
        """
        DESCRIPTION: Log out and log in with the same user
        EXPECTED: Reactivation pop up is displayed
        """
        pass

    def test_004_close_the_pop_up(self):
        """
        DESCRIPTION: Close the pop up
        EXPECTED: * Pop up is closed
        EXPECTED: * User is logged in remaining on home page
        """
        pass

    def test_005__clicktap_account_user_menu_right_hand_menu_mobileverify_the_reactivation_right_hand_menu_item_desktopverify_the_reactivation_user_menu_item(self):
        """
        DESCRIPTION: * Click/tap Account user menu/ Right Hand Menu
        DESCRIPTION: * Mobile:
        DESCRIPTION: Verify the Reactivation Right Hand menu item
        DESCRIPTION: * Desktop:
        DESCRIPTION: Verify the Reactivation User menu item
        EXPECTED: * Account User menu/Right Hand menu is opened
        EXPECTED: * The Reactivation menu item is displayed
        """
        pass

    def test_006_clicktap_the_reactivation_user_menuright_hand_menu_item(self):
        """
        DESCRIPTION: Click/tap the Reactivation User menu/Right Hand menu item
        EXPECTED: User is redirected to Reactivation page within app
        """
        pass

    def test_007_clicktap_back_button(self):
        """
        DESCRIPTION: Click/tap 'Back' button
        EXPECTED: User is navigated to the previous page e.g.:
        EXPECTED: - Home page (mobile)
        EXPECTED: - 'My Account' page (desktop)
        """
        pass
