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
class Test_C440236_Tracking_of_VIP_Feature_on_the_Right_Hand_Menu(Common):
    """
    TR_ID: C440236
    NAME: Tracking of VIP Feature on the Right Hand Menu
    DESCRIPTION: This Test Case verifies tracking in the Google Analytic's data Layer VIP Feature on the Right Hand Menu
    DESCRIPTION: **Jira ticket**
    DESCRIPTION: * BMA-19298 Google Analytics Tracking for VIP Feature
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: VIP IMS Level Configuration:
    PRECONDITIONS: * Non-VIP players = IMS VIP Level 1 - 10
    PRECONDITIONS: * **Bronze** players = IMS VIP Level 11
    PRECONDITIONS: * **Silver** players = IMS VIP Level 12
    PRECONDITIONS: * **Gold** players = IMS VIP Level 13
    PRECONDITIONS: * **Platinum** players = IMS VIP Level 14
    """
    keep_browser_open = True

    def test_001_log_in_as_a_vip_user_check_preconditions_for_vip_level_details(self):
        """
        DESCRIPTION: Log in as a VIP user (check Preconditions for VIP level details)
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_the_balance_button_in_order_to_open_the_right_hand_menu(self):
        """
        DESCRIPTION: Tap on the balance button in order to open the Right Hand Menu
        EXPECTED: Right Hand Menu slides out
        """
        pass

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'mobile nav',
        EXPECTED: 'eventAction' : 'open'
        EXPECTED: });
        """
        pass

    def test_004_tap_the_more_info_link(self):
        """
        DESCRIPTION: Tap the 'More Info' link
        EXPECTED: VIP User is redirected to the VIP page
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'mobile nav',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'more info'
        EXPECTED: });
        """
        pass

    def test_006_repeat_steps_1_5_for_the_following_users_bronze_silver_gold_platinum(self):
        """
        DESCRIPTION: Repeat steps 1-5 for the following users:
        DESCRIPTION: * Bronze
        DESCRIPTION: * Silver
        DESCRIPTION: * Gold
        DESCRIPTION: * Platinum
        EXPECTED: 
        """
        pass

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_008_log_in_as_not_a_vip_user_check_preconditions_for_vip_level_details(self):
        """
        DESCRIPTION: Log in as NOT a VIP user (check Preconditions for VIP level details)
        EXPECTED: User is logged in
        """
        pass

    def test_009_tap_on_the_balance_button_in_order_to_open_the_right_hand_menu(self):
        """
        DESCRIPTION: Tap on the balance button in order to open the Right Hand Menu
        EXPECTED: * Right Hand Menu slides out
        EXPECTED: * The menu does not include a VIP summary
        EXPECTED: * The menu does not include VIP Points
        """
        pass

    def test_010_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: "dataLayer" object is not sent to the GA for 'Open' action
        """
        pass
