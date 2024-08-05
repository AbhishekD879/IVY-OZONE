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
class Test_C363807_Tracking_of_International_Tote_Racing_Post_Summary(Common):
    """
    TR_ID: C363807
    NAME: Tracking of International Tote Racing Post Summary
    DESCRIPTION: This Test Case verifies tracking in the Google Analytic's data Layer due user clicks on 'Show Summary' on the International Tote Event Details page.
    DESCRIPTION: **Jira ticket**
    DESCRIPTION: * BMA-19374 International Tote: Google Analytics Tracking
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Racing Post Summary should be available on International Tote Event Details page
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_international_tote_and_open_any_event_details_page(self):
        """
        DESCRIPTION: Navigate to the International Tote and open any Event Details page
        EXPECTED: * International Tote Event Details page is opened
        EXPECTED: * Racing Post Summaries are shown for each selection
        """
        pass

    def test_003_click_on_plus_symbol_near_some_selection(self):
        """
        DESCRIPTION: Click on '+' symbol near some selection
        EXPECTED: * 'Racing Post Summary' is shown
        EXPECTED: * 'Racing Post Summary' section is expanded
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'international tote',
        EXPECTED: 'eventAction' : 'show summary',
        EXPECTED: });
        """
        pass

    def test_005_click_on___symbol_near_the_same_selection(self):
        """
        DESCRIPTION: Click on '-' symbol near the same selection
        EXPECTED: * 'Racing Post Summary' is hidden
        EXPECTED: * 'Racing Post Summary' section is collapsed
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'international tote',
        EXPECTED: 'eventAction' : 'hide summary',
        EXPECTED: });
        """
        pass

    def test_007_repeat_steps_1_6_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-6 for Logged In user
        EXPECTED: 
        """
        pass
