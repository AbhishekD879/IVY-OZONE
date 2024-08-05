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
class Test_C1790397_Tracking_of_clicks_on_the_footer_links(Common):
    """
    TR_ID: C1790397
    NAME: Tracking of clicks on the footer links
    DESCRIPTION: This test case verifies GA tracking of clicks on the 'footer links' of featured event.
    PRECONDITIONS: * Test case should be run on Desktop.
    PRECONDITIONS: * Browser console should be opened.
    PRECONDITIONS: * The 'Featured Event' area is opened and contains more than one event.
    PRECONDITIONS: (CMS Configurable https://coral-cms-dev0.symphony-solutions.eu/featured-modules )
    """
    keep_browser_open = True

    def test_001_navigate_to_the_featured_events_tab_and_click_on_view_all_events(self):
        """
        DESCRIPTION: Navigate to the featured events tab and click on "View all Events".
        EXPECTED: All Events page opens
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'.
        EXPECTED: A few events corresponding to each click have been created in dataLayer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'featured events',
        EXPECTED: 'eventLabel' : 'view all'
        EXPECTED: })
        """
        pass
