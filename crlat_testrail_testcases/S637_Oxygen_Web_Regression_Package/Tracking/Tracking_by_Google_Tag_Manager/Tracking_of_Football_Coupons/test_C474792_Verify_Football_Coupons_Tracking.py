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
class Test_C474792_Verify_Football_Coupons_Tracking(Common):
    """
    TR_ID: C474792
    NAME: Verify Football Coupons Tracking
    DESCRIPTION: This test case verifies Football Coupons Tracking
    PRECONDITIONS: Dev Tools -> Console should be opened
    PRECONDITIONS: *NOTE:*
    PRECONDITIONS: COUPON NAME - This is what coupon the user sees and selects on site
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        pass

    def test_003_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: * 'Coupons' tab is selected and highlighted
        EXPECTED: * Coupons Landing page is loaded
        EXPECTED: * List of coupons is displayed on the Coupons Landing page
        """
        pass

    def test_004_choose_any_coupon_from_list_on_coupons_landing_page(self):
        """
        DESCRIPTION: Choose any coupon from list on Coupons Landing page
        EXPECTED: Coupon Details page is loaded
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Coupon Selector',
        EXPECTED: 'eventAction' : 'Select Coupon',
        EXPECTED: 'eventLabel' : '<< COUPON NAME >>',
        EXPECTED: });
        """
        pass

    def test_006_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: * 'Matches' page is loaded
        EXPECTED: * 'Coupons' switcher is selected by default and highlighted
        EXPECTED: * List of coupons is displayed on the Coupons Landing page
        """
        pass

    def test_007_repeat_steps_4_6_for_all_available_coupons_received_in_response_from_ob(self):
        """
        DESCRIPTION: Repeat steps 4-6 for all available coupons received in response from OB
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Coupon Selector',
        EXPECTED: 'eventAction' : 'Select Coupon',
        EXPECTED: 'eventLabel' : '<< COUPON NAME >>',
        EXPECTED: });
        """
        pass

    def test_008_tap_change_coupon_selector_link_on_coupons_sub_header(self):
        """
        DESCRIPTION: Tap 'Change coupon' Selector link on Coupons sub-header
        EXPECTED: * List of all available coupons received in response from OB is displayed
        EXPECTED: * The coupon list drop overlay cascades down the page
        """
        pass

    def test_009_choose_any_coupon_from_list_on_coupons_landing_page(self):
        """
        DESCRIPTION: Choose any coupon from list on Coupons Landing page
        EXPECTED: Coupon Details page is loaded
        """
        pass

    def test_010_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: * 'Matches' page is loaded
        EXPECTED: * 'Coupons' switcher is selected by default and highlighted
        EXPECTED: * List of coupons is displayed on the Coupons Landing page
        """
        pass

    def test_011_repeat_steps_8_10_for_all_available_coupons_received_in_response_from_ob(self):
        """
        DESCRIPTION: Repeat steps 8-10 for all available coupons received in response from OB
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Coupon Selector',
        EXPECTED: 'eventAction' : 'Select Coupon',
        EXPECTED: 'eventLabel' : '<< COUPON NAME >>',
        EXPECTED: });
        """
        pass
