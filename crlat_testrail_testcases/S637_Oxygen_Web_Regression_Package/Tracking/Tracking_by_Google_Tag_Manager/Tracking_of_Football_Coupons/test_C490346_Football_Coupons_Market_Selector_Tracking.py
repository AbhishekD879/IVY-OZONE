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
class Test_C490346_Football_Coupons_Market_Selector_Tracking(Common):
    """
    TR_ID: C490346
    NAME: Football Coupons Market Selector Tracking
    DESCRIPTION: This Test Case verifies tracking of Coupons Market Selector usage by users
    PRECONDITIONS: 1. Console is opened
    PRECONDITIONS: 2. To verify tracking on real devices please use following instruction: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: 3. MARKET NAME - This is what market the customer sees and selects on site
    PRECONDITIONS: 4. OPENBET CATEGORY ID - This is the Sport on which the market selector was used. For Football Coupons always will be a football category ID
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_go_to_football___coupons_landing_page(self):
        """
        DESCRIPTION: Load Oxygen application and go to Football -> Coupons landing page
        EXPECTED: 
        """
        pass

    def test_002_select_coupon_from_coupons_list_and_tap_it(self):
        """
        DESCRIPTION: Select Coupon from Coupons list and tap it
        EXPECTED: - Coupon Details page is opened
        EXPECTED: - Coupon Market Selector is displayed on the page
        """
        pass

    def test_003_tap_coupons_market_selector_and_select_market_from_the_listgo_to_console___datalayer_and_verify_tracking_data_for_the_selector(self):
        """
        DESCRIPTION: Tap Coupons Market selector and select Market from the list.
        DESCRIPTION: Go to Console -> DataLayer and verify tracking data for the Selector
        EXPECTED: Following data are displayed in DataLater:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'market selector',
        EXPECTED: 'eventAction' : 'change market',
        EXPECTED: 'eventLabel' : '<< MARKET NAME >>',
        EXPECTED: 'categoryID' : '<< OPENBET CATEGORY ID >>'
        EXPECTED: });
        """
        pass

    def test_004_repeat_step_3_for_different_markets_and_for_different_coupons(self):
        """
        DESCRIPTION: Repeat step 3 for different markets and for different Coupons
        EXPECTED: 
        """
        pass
