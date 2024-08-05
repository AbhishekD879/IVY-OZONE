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
class Test_C440335_GA_Tracking_on_VIP_page(Common):
    """
    TR_ID: C440335
    NAME: GA Tracking on VIP page
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

    def test_003_tap_the_more_info_link(self):
        """
        DESCRIPTION: Tap the 'More Info' link
        EXPECTED: VIP User is redirected to the VIP page
        """
        pass

    def test_004_click_on_hideshow_checkbox_near_hide_vip_status_from_my_account_menu(self):
        """
        DESCRIPTION: Click on 'hide/show' checkbox near 'Hide VIP Status from My Account Menu'
        EXPECTED: * Checkbox near 'Hide VIP Status from My Account Menu' is checked
        EXPECTED: * 'Points Meter' and 'Total Number of Priority' are hidden from the VIP Summary on the Right Hand Menu
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'vip',
        EXPECTED: 'eventAction' : 'hide',
        EXPECTED: 'eventLabel' : 'points'
        EXPECTED: });
        """
        pass

    def test_006_click_on_hideshow_checkbox_near_hide_vip_status_from_my_account_menu_one_more_time(self):
        """
        DESCRIPTION: Click on 'hide/show' checkbox near 'Hide VIP Status from My Account Menu' one more time
        EXPECTED: * Checkbox near 'Hide VIP Status from My Account Menu' is unchecked
        EXPECTED: * 'Points Meter' and 'Total Number of Priority' are shown on the VIP Summary on the Right Hand Menu
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'vip',
        EXPECTED: 'eventAction' : 'show',
        EXPECTED: 'eventLabel' : 'points'
        EXPECTED: });
        """
        pass

    def test_008_click_on_exclusive_promotion_button(self):
        """
        DESCRIPTION: Click on 'Exclusive Promotion' button
        EXPECTED: User is redirected to the Promotion page
        """
        pass

    def test_009_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'vip',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'promotions'
        EXPECTED: });
        """
        pass

    def test_010_navigate_again_to_the_vip_page(self):
        """
        DESCRIPTION: Navigate again to the VIP page
        EXPECTED: * VIP page is opened
        EXPECTED: * VIP level description is expanded by default
        """
        pass

    def test_011_tap_on_expanded_vip_level_description(self):
        """
        DESCRIPTION: Tap on expanded VIP level description
        EXPECTED: VIP level description is collapsed
        """
        pass

    def test_012_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'vip',
        EXPECTED: 'eventAction' : 'hide',
        EXPECTED: 'eventLabel' : '<< VIP LEVEL >>'
        EXPECTED: });
        """
        pass

    def test_013_verify_eventlabel_parameter_that_present_in_current_object_in_datalayer_(self):
        """
        DESCRIPTION: Verify 'eventLabel' parameter that present in current object in 'dataLayer' :
        EXPECTED: 'eventLabel' = depends on expanded/collapsed VIP level description
        """
        pass

    def test_014_tap_on_collapsed_vip_level_description(self):
        """
        DESCRIPTION: Tap on collapsed VIP level description
        EXPECTED: VIP level description is expanded
        """
        pass

    def test_015_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'vip',
        EXPECTED: 'eventAction' : 'show',
        EXPECTED: 'eventLabel' : '<< VIP LEVEL >>'
        EXPECTED: });
        """
        pass

    def test_016_verify_eventlabel_parameter_that_present_in_current_object_in_datalayer_(self):
        """
        DESCRIPTION: Verify 'eventLabel' parameter that present in current object in 'dataLayer' :
        EXPECTED: 'eventLabel' = depends on expanded/collapsed VIP level description
        """
        pass

    def test_017_repeat_steps_11_16_for_the_following_vip_levels_description_bronze_silver_gold_platinum(self):
        """
        DESCRIPTION: Repeat steps 11-16 for the following VIP levels description:
        DESCRIPTION: * Bronze
        DESCRIPTION: * Silver
        DESCRIPTION: * Gold
        DESCRIPTION: * Platinum
        EXPECTED: 
        """
        pass

    def test_018_repeat_steps_1_17_for_the_following_users_bronze_silver_gold_platinum(self):
        """
        DESCRIPTION: Repeat steps 1-17 for the following users:
        DESCRIPTION: * Bronze
        DESCRIPTION: * Silver
        DESCRIPTION: * Gold
        DESCRIPTION: * Platinum
        EXPECTED: 
        """
        pass
