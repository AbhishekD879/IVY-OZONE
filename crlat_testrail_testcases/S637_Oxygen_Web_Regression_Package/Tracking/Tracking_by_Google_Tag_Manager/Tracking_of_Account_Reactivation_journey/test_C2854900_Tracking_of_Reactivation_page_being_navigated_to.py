import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2854900_Tracking_of_Reactivation_page_being_navigated_to(Common):
    """
    TR_ID: C2854900
    NAME: Tracking of Reactivation page being navigated to
    DESCRIPTION: This test case verifies tracking of Reactivation page being navigated to
    PRECONDITIONS: * User's Account is closed (Navigate to Right Menu -> My Account -> select Responsible Gambling item -> Tap/click 'I want to close my Account' link within 'Account Closure' section)
    PRECONDITIONS: * Player Tag - 'Account_Closed_By_Player' is set to 'True' for a user in IMS
    PRECONDITIONS: * Player Tag 'On_login_Account_Closed_Message' is set for a user in IMS
    PRECONDITIONS: * “Reactivation” Log in message is created with the tag 'On_login_Account_Closed_Message' in IMS
    PRECONDITIONS: * The on login pop up is set within IMS - configuration instructions can be found here https://drive.google.com/drive/u/2/folders/1pkGIbDBUp2rU_iWXh1ve18W0mwK71VMU
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * On login 'Reactivation' pop up is displayed
    """
    keep_browser_open = True

    def test_001_navigate_to_reactivation_page_via_on_login_pop_up_url(self):
        """
        DESCRIPTION: Navigate to 'Reactivation' page via on login pop up url
        EXPECTED: 'Reactivation' page is displayed
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackPageview', 'page' : '/gambling-controls/account-reactivation/step-1' }
        """
        pass

    def test_003_clicktap_back_button(self):
        """
        DESCRIPTION: Click/tap 'Back' button
        EXPECTED: User is navigated to Home page
        """
        pass

    def test_004_clicktap_account_user_menu(self):
        """
        DESCRIPTION: Click/tap account user menu
        EXPECTED: * Account user menu is opened
        EXPECTED: * The Reactivation menu item is displayed
        """
        pass

    def test_005_clicktap_the_reactivation_user_menu_item(self):
        """
        DESCRIPTION: Click/tap the Reactivation user menu item
        EXPECTED: User is redirected to Reactivation page within app
        """
        pass

    def test_006_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass
