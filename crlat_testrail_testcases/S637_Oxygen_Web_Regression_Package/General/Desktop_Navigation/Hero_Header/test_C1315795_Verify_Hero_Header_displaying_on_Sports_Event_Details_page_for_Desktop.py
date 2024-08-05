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
class Test_C1315795_Verify_Hero_Header_displaying_on_Sports_Event_Details_page_for_Desktop(Common):
    """
    TR_ID: C1315795
    NAME: Verify Hero Header displaying on Sports Event Details page for Desktop
    DESCRIPTION: This test case verifies Hero Header displaying on Sports Event Details page for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Sports Event Details page is opened
    PRECONDITIONS: **Link to pre-match stats related info:** https://confluence.egalacoral.com/display/SPI/Football+Pre-match+Statistics
    """
    keep_browser_open = True

    def test_001_verify_sports_hero_header_content_on_the_event_details_page(self):
        """
        DESCRIPTION: Verify Sports Hero Header content on the Event Details page
        EXPECTED: Main View 1 and Main View 2 columns are merged and contain the following element:
        EXPECTED: * Sport header with 'Back' button, 'Favorites' icon (for Football only), Event name and Start time of event (Also 'Live' label is displayed before Start time if it's live event)
        EXPECTED: * Breadcrumbs trail
        EXPECTED: * Statistic (Football) for pre-match event and Visualization (Football and Tennis) or Scoreboard (Football, Tennis, Basketball, Cricket, Darts, Rugby) for live event (if available)
        EXPECTED: * Enhanced Multiples Caurosel (only for pre-match event if available)
        EXPECTED: * Markets tabs menu
        """
        pass

    def test_002_verify_breadcrumbs_trail_displaying(self):
        """
        DESCRIPTION: Verify Breadcrumbs trail displaying
        EXPECTED: * Breadcrumbs trail is displayed below Sports header
        EXPECTED: * Breadcrumbs trail is displayed in the next format: 'Home' &gt; 'Sports Name' &gt; 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_003_verify_enhanced_multiples_carousel_displaying(self):
        """
        DESCRIPTION: Verify Enhanced Multiples carousel displaying
        EXPECTED: * Enhanced Multiples carousel is displayed below Breadcrumbs trail (or below Pre-match statistic if it's available)
        EXPECTED: * Enhanced Multiples carousel contains separated sports cards that are scrolled to right and left side
        EXPECTED: * Enhanced Multiples carousel is not displayed at all in case there are no available Enhanced Multiples events
        """
        pass

    def test_004_verify_markets_tabs_menu_displaying(self):
        """
        DESCRIPTION: Verify Markets tabs menu displaying
        EXPECTED: * Market tabs are displayed below EM carousel (if EM events are available)
        EXPECTED: * Market tabs are scrolled to right and left side by using Navigation arrows
        """
        pass
