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
class Test_C2024351_Tracking_of_clicking_on_View_All_link_at_HR_Virtuals_widget(Common):
    """
    TR_ID: C2024351
    NAME: Tracking of clicking on 'View All' link at HR 'Virtuals' widget
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'View All' link at 'Virtuals' widget on HR Landing page.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_the_horse_race_landing_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Race' Landing page
        EXPECTED: 'Horse Racing' Landing page is opened
        """
        pass

    def test_003_scroll_the_page_down_to_the_inspired_virtuals_widget(self):
        """
        DESCRIPTION: Scroll the page down to the inspired 'Virtuals' widget
        EXPECTED: Inspired 'Virtuals' widget is shown as the carousel in 3rd column or below main content (depends on screen resolution)
        """
        pass

    def test_004_click_on_the_view_all_link_in_the_footer_below_event_cards(self):
        """
        DESCRIPTION: Click on the 'View All' link in the footer below event cards
        EXPECTED: User is redirected to the 'Inspired virtual' page > first available event details tab
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'virtuals',
        EXPECTED: 'eventLabel' : 'view all'
        EXPECTED: })
        """
        pass
