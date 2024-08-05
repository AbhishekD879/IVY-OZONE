import pytest
import tests
from tests.base_test import vtest
from collections import OrderedDict
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.navigation
@vtest
class Test_C1315795_Verify_Hero_Header_displaying_on_Sports_Event_Details_page_for_Desktop(BasePrivateMarketsTest, BaseSportTest):
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
    expected_breadcrumbs = ['Home', 'Football']
    device_name = tests.desktop_default

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
        self.user = tests.settings.default_username
        self.site.login(username=self.user)
        event_params = self.ob_config.add_football_event_to_england_premier_league()

        self.__class__.eventID = event_params.event_id
        self.site.wait_content_state("homepage")
        event_params = self.ob_config.add_football_event_enhanced_multiples()

        self.__class__.eventID2 = event_params.event_id

    def test_002_verify_breadcrumbs_trail_displaying(self):
        """
        DESCRIPTION: Verify Breadcrumbs trail displaying
        EXPECTED: * Breadcrumbs trail is displayed below Sports header
        EXPECTED: * Breadcrumbs trail is displayed in the next format: 'Home' > 'Sports Name' > 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        page = self.site.football
        breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                  for key in page.breadcrumbs.items_as_ordered_dict)
        self.assertTrue(self.site.football.header_line.back_button, msg='Back button is not present')
        if self.brand == 'bma':
            self.assertTrue(self.site.football.header_line.go_to_favourites_page, msg='Favourites button is not present')
        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

    def test_003_verify_enhanced_multiples_carousel_displaying(self):
        """
        DESCRIPTION: Verify Enhanced Multiples carousel displaying
        EXPECTED: * Enhanced Multiples carousel is displayed below Breadcrumbs trail (or below Pre-match statistic if it's available)
        EXPECTED: * Enhanced Multiples carousel contains separated sports cards that are scrolled to right and left side
        EXPECTED: * Enhanced Multiples carousel is not displayed at all in case there are no available Enhanced Multiples events
        """
        self.navigate_to_edp(event_id=self.eventID2, sport_name='football')
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID2,
                                                               query_builder=self.ss_query_builder)
        accordion_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        self.assertIn('ENHANCED MULTIPLES', accordion_name, msg=f'"{accordion_name} is not Enhanced Multiples"')

    def test_004_verify_markets_tabs_menu_displaying(self):
        """
        DESCRIPTION: Verify Markets tabs menu displaying
        EXPECTED: * Market tabs are displayed below EM carousel (if EM events are available)
        EXPECTED: * Market tabs are scrolled to right and left side by using Navigation arrows
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        subtabs = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(subtabs, msg='No subtabs found')
