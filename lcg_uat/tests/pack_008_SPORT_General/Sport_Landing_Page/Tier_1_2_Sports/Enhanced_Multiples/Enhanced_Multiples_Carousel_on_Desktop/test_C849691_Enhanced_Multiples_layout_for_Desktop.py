import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can't create OB event on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.enhanced_multiples
@pytest.mark.sports
@vtest
class Test_C849691_Enhanced_Multiples_layout_for_Desktop(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C849691
    NAME: Enhanced Multiples layout for Desktop
    DESCRIPTION: This test case verifies Enhanced Multiples layout for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Make sure you have  Enhanced Multiples events on some sports (Sports events with typeName="Enhanced Multiples")
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. Enhanced Multiples are not available for Lotto and Virtuals.
    PRECONDITIONS: 2. Enhanced Multiples layout remains unchanged for tablet and mobile (EM events are displayed in accordions).
    PRECONDITIONS: 3. For each Class retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: XXX - is a comma-separated list of **Class **ID's;
    PRECONDITIONS: XX - sports **Category **ID
    PRECONDITIONS: X.XX - current supported version of the OpenBet release
    PRECONDITIONS: ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    sport_name = vec.bma.TENNIS
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football enhanced multiples event
        """
        event_params_1 = self.ob_config.add_football_event_enhanced_multiples(is_live=False)
        self.__class__.event_name = event_params_1.team1 + " v " + event_params_1.team2
        self.__class__.eventID2 = event_params_1.event_id
        event_params_2 = self.ob_config.add_football_event_enhanced_multiples(is_live=True)
        self.__class__.eventID3 = event_params_2.event_id

    def test_001_navigate_to_sports_landing_page_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to Sports Landing page where Enhanced Multiples events are present
        EXPECTED:   <Sports> Landing Page is opened
        EXPECTED:  Event cards are displayed within 'Enhanced Multiples' carousel on the whole width of the section
        """
        self.site.wait_content_state('homepage')
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        current_tab_name = self.site.football.tabs_menu.current
        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is not "{expected_tab_name}", it is "{current_tab_name}"')
        actual_date_tab_name = self.site.football.date_tab.current_date_tab
        self.assertEqual(actual_date_tab_name, vec.sb.SPORT_DAY_TABS.today,
                         msg=f'Actual date tab is "{actual_date_tab_name}" not "{vec.sb.SPORT_DAY_TABS.today}"')

    def test_002_verify_enhanced_multiples_events(self):
        """
        DESCRIPTION: Verify 'Enhanced Multiples' events
        EXPECTED:  'Enhanced Multiples' events are displayed in carousel below banner area
        EXPECTED:  Each event card in carousel contains label 'Enhanced' in the top left corner
        """
        banner_section = self.site.football.aem_banner_section
        self.assertTrue(banner_section, msg='Banner section is not present')
        banner_coordinates = banner_section.location.get('y')

        em_carousel = self.site.football.sport_enhanced_multiples_carousel
        self.assertTrue(em_carousel, msg='Enhanced Multiples carousel is not displayed')
        self.assertTrue(banner_coordinates < em_carousel.location.get('y'),
                        msg='Enhanced Multiples carousel is not displayed below AEM banners')
        self.assertTrue(em_carousel.items_as_ordered_dict, msg='No event sections are present on page')

    def test_003_navigate_to_any_sports_page_where_only_one_enhanced_multiples_event_is_present(self):
        """
        DESCRIPTION: Navigate to any <Sports> page where only one Enhanced Multiples event is present
        EXPECTED:   <Sports> Landing Page is opened
        EXPECTED:  Only one card is displayed within 'Enhanced Multiples' carousel on the whole width of the section
        """
        # Can not automate as we may get multiple events on carousel

    def test_004_navigate_to_any_sports_page_where_enhanced_multiples_events_are_not_present(self):
        """
        DESCRIPTION: Navigate to any <Sports> page where Enhanced Multiples events are NOT present
        EXPECTED:   <Sports> Landing Page is opened
        EXPECTED:  'Enhanced Multiples' carousel is NOT displayed
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state(state_name=self.sport_name, timeout=30)
        self.site.wait_splash_to_hide(timeout=10)
        self.device.driver.implicitly_wait(3)
        current_tab = self.site.tennis.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                         msg=f'Default tab: "{current_tab}" opened'
                             f'Expected tab: "{self.expected_sport_tabs.matches}" opened')
        # can not verify 'Enhanced Multiples' carousel which is not present on UI

    def test_005_repeat_steps_2_4_on_sports_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: Repeat steps 2-4 on <Sports> Event Details Page but only for Pre-match events
        EXPECTED:   <Sports> Event Details Page is opened
        EXPECTED:  'Enhanced Multiples' events are displayed within carousel below Stats (if applicable) or 'Breadcrumbs' trail
        """
        self.navigate_to_edp(event_id=self.eventID2, sport_name='football')
        expected_breadcrumbs = ['Home', 'Football', self.event_name]
        breadcrumbs = self.site.sport_event_details.breadcrumbs
        self.assertTrue(breadcrumbs, msg='Breadcrumbs trail is not present')
        self.assertTrue(breadcrumbs.items_as_ordered_dict, msg='No breadcrumbs found')
        actual_breadcrumbs = list(breadcrumbs.items_as_ordered_dict.keys())
        self.assertEqual(actual_breadcrumbs, expected_breadcrumbs,
                         msg=f'Breadcrumbs {actual_breadcrumbs} are not the same '
                             f'as expected {expected_breadcrumbs}')

    def test_006_navigate_to_sports_event_details_page_but_for_live_events(self):
        """
        DESCRIPTION: Navigate to <Sports> Event Details Page but for LIVE events
        EXPECTED:   <Sports> Event Details Page is opened
        EXPECTED:  'Enhanced Multiples' carousel is NOT displayed
        """
        self.navigate_to_edp(event_id=self.eventID3, sport_name='football')
        # can not verify  'Enhanced Multiples' carousel which is not present on UI

    def test_007_repeat_steps_2_4_on_homepage(self):
        """
        DESCRIPTION: Repeat steps 2-4 on Homepage
        EXPECTED:
        """
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        banner_section = self.site.home.aem_banner_section
        self.assertTrue(banner_section, msg='Banner section is not present')
        banner_coordinates = banner_section.location.get('y')
        em_carousel = self.site.home.desktop_modules.enhanced_module
        self.assertTrue(em_carousel, msg='Enhanced Multiples carousel is not displayed')
        self.assertTrue(banner_coordinates < em_carousel.location.get('y'),
                        msg='Enhanced Multiples carousel is not displayed below AEM banners')
