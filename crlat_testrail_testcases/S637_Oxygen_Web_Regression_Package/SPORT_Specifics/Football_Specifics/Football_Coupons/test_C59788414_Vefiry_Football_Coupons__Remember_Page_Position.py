import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C59788414_Vefiry_Football_Coupons__Remember_Page_Position(Common):
    """
    TR_ID: C59788414
    NAME: Vefiry Football Coupons - Remember Page Position
    DESCRIPTION: This test case verifies navigation from a football coupon page to an EDP and back.
    PRECONDITIONS: 1. In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: Load Oxygen application - Homepage is opened
    PRECONDITIONS: COUPONS for Coral (CMS configurable)
    PRECONDITIONS: ACCAS for Ladbrokes (CMS configurable)
    """
    keep_browser_open = True

    def test_001_load_the_app_and_go_to_the_football_landing_page___coupons_tab(self):
        """
        DESCRIPTION: Load the app and Go to the Football Landing page -> 'Coupons' tab.
        EXPECTED: Coupons Landing page is loaded
        EXPECTED: List of coupons is displayed on the Coupons Landing page
        """
        pass

    def test_002_choose_some_football_coupon_eg_uk_coupon(self):
        """
        DESCRIPTION: Choose some Football Coupon (e.g UK Coupon)
        EXPECTED: Events for selected coupon are displayed on Coupons Details page
        """
        pass

    def test_003_select_any_event_from_the_list_on_the_page_and_navigate_to_edp(self):
        """
        DESCRIPTION: Select any event from the list on the page and Navigate to EDP.
        EXPECTED: EDP is loaded correctly.
        """
        pass

    def test_004_return_back_to_the_previous_pageuse_all_back_journeys_ie_breadcrumbs_a_back_button_for_browser_and_android_back_button_etc(self):
        """
        DESCRIPTION: Return back to the previous page.
        DESCRIPTION: Use all "back" journeys i.e. breadcrumbs, a back button for browser and android back button etc.
        EXPECTED: Football coupon page opens on the remembered position from step3.
        EXPECTED: App remembered position where a user was on the coupon page when the user navigates back.
        """
        pass
