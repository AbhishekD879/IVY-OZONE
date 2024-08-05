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
class Test_C1790396_Tracking_of_clicks_on_the_Additional_Market_links(Common):
    """
    TR_ID: C1790396
    NAME: Tracking of clicks on the 'Additional Market' links
    DESCRIPTION: This test case verifies GA tracking of clicks on the 'Additional Market' links of featured event.
    PRECONDITIONS: * Test case should be run on Desktop.
    PRECONDITIONS: * Browser console should be opened.
    PRECONDITIONS: * User is logged in.
    PRECONDITIONS: * The 'Featured Event' area is opened and contains the 'Additional Market' link.
    PRECONDITIONS: (CMS Configurable https://coral-cms-dev0.symphony-solutions.eu/featured-modules )
    """
    keep_browser_open = True

    def test_001_navigate_to_the_featured_event_area_and_click_on_the_additional_market_link(self):
        """
        DESCRIPTION: Navigate to the featured event area and click on the 'Additional Market' link.
        EXPECTED: The 'Additional Market' page opens with the 'Main Market' tab pre-selected.
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: A few events corresponding to each click have been created in dataLayer and includes:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'featured events',
        EXPECTED: 'eventLabel' : 'additional markets'
        EXPECTED: })
        """
        pass

    def test_003__navigate_to_featured_modules_created_in_cms_by_type_id_race_id_race_grid_selection_id_enhanced_multiples_id_repeat_step_1__2(self):
        """
        DESCRIPTION: * Navigate to Featured Modules created in CMS by: Type ID, Race ID, Race Grid, Selection ID, Enhanced Multiples ID.
        DESCRIPTION: * Repeat step 1 & 2
        EXPECTED: 
        """
        pass

    def test_004_log_out__repeat_steps_1___3(self):
        """
        DESCRIPTION: Log out & repeat steps 1 - 3
        EXPECTED: A few events corresponding to each click have been created in dataLayer and includes:
        EXPECTED: 'event': "logout", success: "true",
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'featured events',
        EXPECTED: 'eventLabel' : 'additional markets'
        EXPECTED: })
        """
        pass
