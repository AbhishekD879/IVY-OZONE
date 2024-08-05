import pytest
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can't create OB event on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.enhanced_multiples
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C28466_Verify_Filtering_of_Enhanced_Multiples_Events(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28466
    NAME: Verify Filtering of Enhanced Multiples Events
    DESCRIPTION: This test case verifies Filtering of Enhanced Multiples Events.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: **NOTE: Make sure you have  Enhanced Multiples events on Some sports (Sport events with typeName="Enhanced Multiples").**
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. For each Class retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XXX - is a comma separated list of **Class **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. For each Type retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   XXX - is a comma separated list of **Type **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH)
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4. In order to check particular event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    selection_type = "all to win in 90 Mins"
    selection_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football enhanced multiples event
        """
        event_params = self.ob_config.add_football_event_enhanced_multiples()
        team1, team2, self.__class__.selection_ids = \
            event_params.team1, event_params.team2, event_params.selection_ids
        self.__class__.selection_name = f'{team1}, {team2} {self.selection_type}'
        self.__class__.type_id = self.ob_config.football_config.specials.enhanced_multiples.type_id

        event_params_1 = self.ob_config.add_football_event_enhanced_multiples()
        self.__class__.eventID2 = event_params_1.event_id

        self.__class__.events_filter = self.basic_active_events_filter().add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.EQUALS, "|Enhanced Multiples|"))

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('homepage')

    def test_002_navigate_to_any_sports_page_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to any <Sports> page where Enhanced Multiples events are present
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        current_tab_name = self.site.football.tabs_menu.current
        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is not "{expected_tab_name}", it is "{current_tab_name}"')
        if self.device_type == 'desktop':
            actual_date_tab_name = self.site.football.date_tab.current_date_tab
            self.assertEqual(actual_date_tab_name, vec.sb.SPORT_DAY_TABS.today,
                             msg=f'Actual date tab is "{actual_date_tab_name}" not "{vec.sb.SPORT_DAY_TABS.today}"')

    def test_003_verifyenhanced_multiples_section(self):
        """
        DESCRIPTION: Verify 'Enhanced Multiples' section
        EXPECTED: * Expanded 'Enhanced Multiples' section is shown at the top of the 'Type' accordions with Event list for **Mobile/Tablet**
        EXPECTED: * 'Enhanced Multiples' is displayed in carousel below banner area for **Desktop**
        EXPECTED: * Section contains EM outcomes
        """
        if self.device_type == 'mobile':
            sections = self.site.football.tab_content.accordions_list.get_items(name=vec.racing.ENHANCED_MULTIPLES_NAME)
            self.assertTrue(sections, msg='No event sections are present on page')
            self.assertIn(vec.racing.ENHANCED_MULTIPLES_NAME, sections,
                          msg='No "ENHANCED MULTIPLES" section found in list')
            section = sections[vec.racing.ENHANCED_MULTIPLES_NAME]
            section.click()
            section_items = section.items_as_ordered_dict
            self.assertTrue(section_items, msg=f'No events found in event section: "{vec.racing.ENHANCED_MULTIPLES_NAME}"')
            event = section_items.get(self.selection_name)
            self.assertTrue(event, msg=f'Event "{self.selection_name}" not found in {list(section_items.keys())}')
            self.verify_event_time_is_present(event)
            self._verify_event_name(event)
            all_prices = event.get_active_prices()
            self.assertTrue(all_prices, msg=f'Event "{self.selection_name}" does not have active selections')
        else:
            aem_banner_section = self.site.football.aem_banner_section
            self.assertTrue(aem_banner_section, msg='AEM banner section is not present')
            sections = self.site.football.tab_content.accordions_list.get_items(name=vec.racing.ENHANCED_MULTIPLES_NAME)
            self.assertTrue(sections, msg='No event sections are present on page')
            self.assertNotIn(vec.racing.ENHANCED_MULTIPLES_NAME, sections,
                             msg='"ENHANCED MULTIPLES" section found in list')

    def test_004_verify_present_em_outcomes(self):
        """
        DESCRIPTION: Verify present EM Outcomes
        EXPECTED: EM outcomes are shown due to the following rules:
        EXPECTED: *   Just outcomes of events with attribute **typeName="Enhanced Multiples****" **are shown
        EXPECTED: *   Just outcomes of events with **NO isStarted="true"** attribute are shown
        EXPECTED: *   **Each outcome is shown separately **(of events with more then one market and more than one outcome, of  events one market and more than one outcome, of  events with one market and one outcome)
        """
        # step covered into step 3

    def test_005_navigate_to_any_sports_page_where_enhanced_multiples_events_are_not_present(self, tab='today'):
        """
        DESCRIPTION: Navigate to any <Sports> page where Enhanced Multiples events are NOT present
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        self.navigate_to_page('sport/tennis')
        self.site.wait_content_state(state_name='tennis')
        current_tab_name = self.site.tennis.tabs_menu.current
        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is not "{expected_tab_name}", it is "{current_tab_name}"')
        if self.device_type == 'desktop':
            if tab == "today":
                actual_date_tab_name = self.site.tennis.date_tab.current_date_tab
                self.assertEqual(actual_date_tab_name, vec.sb.SPORT_DAY_TABS.today,
                                 msg=f'Actual date tab is "{actual_date_tab_name}" not "{vec.sb.SPORT_DAY_TABS.today}"')
            elif tab == "tomorrow":
                self.site.sports_page.date_tab.tomorrow.click()
                self.assertEqual(self.site.sports_page.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.tomorrow,
                                 msg=f'Current active tab: "{self.site.sports_page.date_tab.current_date_tab}", '
                                     f'expected: "{vec.sb.SPORT_DAY_TABS.tomorrow}"')
            else:
                self.site.sports_page.date_tab.future.click()
                self.assertEqual(self.site.sports_page.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.future,
                                 msg=f'Current active tab: "{self.site.sports_page.date_tab.current_date_tab}", '
                                     f'expected: "{vec.sb.SPORT_DAY_TABS.future}"')

    def test_006_verify_presence_of_enhanced_multiples_section_for_mobiletablet_and_carousel_for_desktop(self):
        """
        DESCRIPTION: Verify presence of  'Enhanced Multiples' section for **Mobile/Tablet** and carousel for **Desktop**
        EXPECTED: 'Enhanced Multiples' section for **Mobile/Tablet** and carousel for **Desktop** is NOT shown
        """
        if self.device_type == 'mobile':
            sections = self.site.tennis.tab_content.accordions_list.get_items(name=vec.racing.ENHANCED_MULTIPLES_NAME)
            self.assertFalse(sections, msg='Event sections are present on page')
        else:
            aem_banner_section = self.site.tennis.aem_banner_section
            self.assertTrue(aem_banner_section, msg='Banner section is present')
            sections = self.site.tennis.tab_content.accordions_list.items_as_ordered_dict
            self.assertIn(vec.racing.ENHANCED_MULTIPLES_NAME, sections,
                          msg='No "ENHANCED MULTIPLES" section found in list')

    def test_007_repeat_steps_3_6_for_tomorrow_tab_for_desktoptablet(self):
        """
        DESCRIPTION: Repeat steps 3-6 for 'Tomorrow' tab for Desktop/Tablet
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        self.test_003_verifyenhanced_multiples_section()
        self.test_005_navigate_to_any_sports_page_where_enhanced_multiples_events_are_not_present(tab="tomorrow")
        self.test_006_verify_presence_of_enhanced_multiples_section_for_mobiletablet_and_carousel_for_desktop()

    def test_008_repeat_steps_3_6_for_future_tab_for_desktoptablet(self):
        """
        DESCRIPTION: Repeat steps 3-6 for 'Future' tab for Desktop/Tablet
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        self.test_003_verifyenhanced_multiples_section()
        self.test_005_navigate_to_any_sports_page_where_enhanced_multiples_events_are_not_present(tab="future")
        self.test_006_verify_presence_of_enhanced_multiples_section_for_mobiletablet_and_carousel_for_desktop()

    def test_009_for_desktoprepeat_steps_3_6_on_sports_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 3-6 on <Sports> Event Details Page but only for Pre-match events
        """
        self.navigate_to_edp(event_id=self.eventID2, sport_name='football')
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID2,
                                                               query_builder=self.ss_query_builder)
        accordion_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        self.assertIn('ENHANCED MULTIPLES', accordion_name, msg=f'"{accordion_name} is not Enhanced Multiples"')
        self.test_005_navigate_to_any_sports_page_where_enhanced_multiples_events_are_not_present(tab='today')
        self.test_006_verify_presence_of_enhanced_multiples_section_for_mobiletablet_and_carousel_for_desktop()

    def test_010_repeat_steps_3_6_on_home_page(self):
        """
        DESCRIPTION: Repeat steps 3-6 on Home page
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   'Enhanced Multiples' are displayed in sections within  'Enhanced Multiples' tab
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel below banner area
        """
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        if self.device_type == 'desktop':
            banner_section = self.site.home.aem_banner_section
            self.assertTrue(banner_section, msg='Banner section is not present')
            banner_coordinates = banner_section.location.get('y')
            em_carousel = self.site.home.desktop_modules.enhanced_module
            self.assertTrue(em_carousel, msg='Enhanced Multiples carousel is not displayed')
            self.assertTrue(banner_coordinates < em_carousel.location.get('y'),
                            msg='Enhanced Multiples carousel is not displayed below AEM banners')
        else:
            resp = self.ss_req.ss_event_for_type(type_id=self.type_id, query_builder=self.events_filter)
            events = [event['event'] for event in resp]
            for event in events:
                self.assertTrue(event['typeName'],
                                msg=f'"Enhanced Multiples" are not displayed in sections"')
        self.test_005_navigate_to_any_sports_page_where_enhanced_multiples_events_are_not_present(tab='today')
        self.test_006_verify_presence_of_enhanced_multiples_section_for_mobiletablet_and_carousel_for_desktop()
