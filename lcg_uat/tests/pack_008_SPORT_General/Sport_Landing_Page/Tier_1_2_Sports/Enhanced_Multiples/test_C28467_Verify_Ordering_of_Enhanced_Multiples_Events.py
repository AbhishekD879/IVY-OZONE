import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can't create OB event on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28467_Verify_Ordering_of_Enhanced_Multiples_Events(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28467
    NAME: Verify Ordering of Enhanced Multiples Events
    DESCRIPTION: This test case verifies Ordering of Enhanced Multiples Events.
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
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    selection_type = "all to win in 90 Mins"

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football enhanced multiples event
        """
        event_params_1 = self.ob_config.add_football_event_enhanced_multiples()
        team1, team2 = event_params_1.team1, event_params_1.team2
        self.__class__.selection_name = f'{team1}, {team2} {self.selection_type}'
        self.__class__.type_id = self.ob_config.football_config.specials.enhanced_multiples.type_id

        event_params_2 = self.ob_config.add_football_event_enhanced_multiples()
        self.__class__.eventID2 = event_params_2.event_id

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

    def test_003_go_to_enhanced_multiples_section_for_mobiletablet_and_carousel_for_desktop(self):
        """
        DESCRIPTION: Go to 'Enhanced Multiples' section for **Mobile/Tablet** and carousel for **Desktop**
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
            enhanced_section_name = self.site.football.sport_enhanced_multiples_carousel.section_header.text
            self.assertEqual(enhanced_section_name, 'ENHANCED',
                             msg=f'Actual is "{enhanced_section_name}" not "ENHANCED"')
            enhanced_section = list(self.site.football.sport_enhanced_multiples_carousel.items_as_ordered_dict.values())
            self.assertTrue(enhanced_section, msg='No event sections are present on page')
            for event in enhanced_section:
                self.assertTrue(event.start_time, msg='Event start time is not present')

    def test_004_verify_em_outcomes_ordering_within_section_for_mobiletablet_and_carousel_for_desktop(self):
        """
        DESCRIPTION: Verify EM Outcomes ordering within section for **Mobile/Tablet** and carousel for **Desktop**
        EXPECTED: **For Mobile**
        EXPECTED: EM Outcomes are ordered by:
        EXPECTED: *   by **StartTime** in ascending of the events they belong to
        EXPECTED: *   if StartTime the same then by selections displayOrder
        EXPECTED: *   if StartTime and displayOrder are the same than **Alphabetically**
        EXPECTED: **For desktop**
        EXPECTED: EM Outcomes are ordered by:
        EXPECTED: *   by **StartTime** in ascending of the events they belong to
        """
        # step covered into step 3

    def test_005_clicktap_on_enhanced_multiples_tab_from_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: Click/Tap on 'Enhanced Multiples' tab from Module Selector Ribbon on the Homepage
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   'Enhanced Multiples' tab is opened
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand section
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel below banner area
        """
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            resp = self.ss_req.ss_event_for_type(type_id=self.type_id, query_builder=self.events_filter)
            events = [event['event'] for event in resp]
            event_id = events[0]['id']
            for event in events:
                self.assertTrue(event['typeName'],
                                msg=f'"Enhanced Multiples" are not displayed in sections"')
            self.navigate_to_edp(event_id=event_id, sport_name='football')
        else:
            aem_banner_section = self.site.home.aem_banner_section
            self.assertTrue(aem_banner_section, msg='AEM banner section is not present')
            sections = self.site.home.desktop_modules.enhanced_module.items_as_ordered_dict
            enhanced_module_list = []
            for section, item in sections.items():
                enhanced_module_name = item.header.text.replace('\n', ' ')
                enhanced_module_list.append(enhanced_module_name)
            self.assertIn('ENHANCED FOOTBALL', enhanced_module_list,
                          msg=f'Category name "FOOTBALL" displayed on "{enhanced_module_list}" card '
                          f'next to "Enhanced" label')

    def test_006_verify_em_outcomes_ordering_within_section_within_the_same_category(self):
        """
        DESCRIPTION: Verify EM Outcomes ordering within section (within the same Category)
        EXPECTED: EM Outcomes are ordered by:
        EXPECTED: *   by **StartTime **in ascending of the events they belong to
        EXPECTED: *   if StartTime the same then by selections displayOrder
        EXPECTED: *   if StartTime and displayOrder are the same than **Alphabetically**
        """
        # step covered into step 5

    def test_007_for_desktoprepeat_steps_3_4_on_sports_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 3-4 on <Sports> Event Details Page but only for Pre-match events
        EXPECTED:
        """
        if self.device_type == 'desktop':
            self.navigate_to_edp(event_id=self.eventID2, sport_name='football')
            enhanced_section_name = self.site.football.sport_enhanced_multiples_carousel.section_header.text
            self.assertEqual(enhanced_section_name, 'ENHANCED',
                             msg=f'Actual is "{enhanced_section_name}" not "ENHANCED"')
            enhanced_section = list(self.site.football.sport_enhanced_multiples_carousel.items_as_ordered_dict.values())
            self.assertTrue(enhanced_section, msg='No event sections are present on page')
            for event in enhanced_section:
                self.assertTrue(event.start_time, msg='Event start time is not present')
