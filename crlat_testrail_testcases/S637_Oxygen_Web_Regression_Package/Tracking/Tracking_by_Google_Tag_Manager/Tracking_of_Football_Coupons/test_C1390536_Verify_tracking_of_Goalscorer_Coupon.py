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
class Test_C1390536_Verify_tracking_of_Goalscorer_Coupon(Common):
    """
    TR_ID: C1390536
    NAME: Verify tracking of Goalscorer Coupon
    DESCRIPTION: This Test Case verified tracking in the Google Analytic's data Layer when visit the goalscorer coupon
    DESCRIPTION: Jira ticket: BMA-24407 Google Analytics - Goalscorer Coupon: GA Tracking
    DESCRIPTION: AUTOTEST [C1497918]
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_football_landing_page(self):
        """
        DESCRIPTION: Navigate to the Football Landing page
        EXPECTED: - Football Landing page
        EXPECTED: - 'Today' tab is opened by default
        """
        pass

    def test_003_navigate_to_the_coupons_tab(self):
        """
        DESCRIPTION: Navigate to the 'Coupons' tab
        EXPECTED: 'Coupons' landing page is opened
        """
        pass

    def test_004_select_goalscorer_coupon(self):
        """
        DESCRIPTION: Select 'Goalscorer coupon'
        EXPECTED: 'Goalscorer coupon' page is opened
        """
        pass

    def test_005_scrolls_down_the_page_and_find_the_event_where_show_all_is_available(self):
        """
        DESCRIPTION: Scrolls down the page and find the event where 'Show All' is available
        EXPECTED: 
        """
        pass

    def test_006_click_on_the_show_all_link(self):
        """
        DESCRIPTION: Click on the 'Show All' link
        EXPECTED: All existing selections are shown
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'goalscorer coupon',
        EXPECTED: 'eventAction' : 'show more',
        EXPECTED: 'eventLabel' : '<< EVENT >>'
        EXPECTED: })
        """
        pass

    def test_008_click_on_the_go_to_event_link(self):
        """
        DESCRIPTION: Click on the 'Go to Event' link
        EXPECTED: Event details page is opened
        """
        pass

    def test_009_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: 1. 'Event details' page is opened
        EXPECTED: 2. The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'goalscorer coupon',
        EXPECTED: 'eventAction' : 'go to event',
        EXPECTED: 'eventLabel' : '<< EVENT >>'
        EXPECTED: })
        """
        pass

    def test_010_repeat_steps_1_9_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-9 for Logged In user
        EXPECTED: 
        """
        pass
