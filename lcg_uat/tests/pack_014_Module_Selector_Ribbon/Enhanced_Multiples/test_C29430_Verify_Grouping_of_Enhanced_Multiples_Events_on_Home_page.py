import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from time import sleep
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't create OB event on prod
# @pytest.mark.hl
@pytest.mark.sports
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C29430_Verify_Grouping_of_Enhanced_Multiples_Events_on_Home_page(Common):
    """
    TR_ID: C29430
    NAME: Verify Grouping of Enhanced Multiples Events on Home page
    DESCRIPTION: This test case verifies Grouping of Enhanced Multiples Events on Home page
    PRECONDITIONS: **NOTE:** The events for Enhanced Multiples should be determined by the **drilldownTagNames="EVFLAG_ES****" **in the SiteServer query.
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
    """
    keep_browser_open = True

    def verify_event_start_time(self, event, event_name, event_id):
        event_time_ui = event.event_time
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id,
                                                               query_builder=self.ss_query_builder)
        event_time_resp = event_resp[0]['event']['startTime']
        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               ui_format_pattern=self.my_bets_event_today_time_format_pattern,
                                                               ss_data=True)
        self.assertEqual(event_time_ui.replace(',', ''), event_time_resp_converted.replace(',', ''),
                         msg=f'Event time of event "{event_name}" on UI "{event_time_ui}" is not the same '
                         f'as got from response "{event_time_resp_converted}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create football and horse race test events
        """
        self.__class__.expected_name_section_list = ['FOOTBALL', 'HORSE RACING']
        event_params = self.ob_config.add_football_event_enhanced_multiples()
        self.__class__.event_name = f'{event_params.team1}, {event_params.team2} all to win in 90 Mins'
        self.__class__.type_id = self.ob_config.football_config.specials.enhanced_multiples.type_id
        self.__class__.eventID = event_params.event_id

        event_params2 = self.ob_config.add_enhanced_multiples_racing_event(number_of_runners=1)
        self.__class__.event_name2 = list(event_params2.selection_ids)[0]
        self.__class__.type_id2 = self.ob_config.horseracing_config.daily_racing_specials.enhanced_multiples.type_id
        self.__class__.eventID2 = event_params2.event_id

        self.__class__.multiples_tab = self.get_ribbon_tab_name('tab-multiples')
        if self.multiples_tab:
            self._logger.debug('*** Enhanced Multiples tab is configured on CMS')
        else:
            raise CmsClientException('No Enhanced Multiples tab configured on CMS')

        self.__class__.events_filter = self.basic_active_events_filter().add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.EQUALS, "|Enhanced Multiples|"))

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_tap_enhanced_multiples_tab_from_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap 'Enhanced Multiples' tab from Module Selector Ribbon
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   'Enhanced Multiples' tab is opened
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand section
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel below banner area
        """
        if self.device_type == 'desktop':
            banner_section = self.site.home.aem_banner_section
            self.assertTrue(banner_section, msg='Banner section is not present')
            self.__class__.banner_coordinates = banner_section.location.get('y')

            em_carousel = self.site.home.desktop_modules.enhanced_module
            self.assertTrue(em_carousel, msg='Enhanced Multiples carousel is not displayed')
            self.assertTrue(self.banner_coordinates < em_carousel.location.get('y'),
                            msg='Enhanced Multiples carousel is not displayed below AEM banners')
        else:
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict[self.multiples_tab].click()
            sections = self.site.home.get_module_content(self.multiples_tab).accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg=f'*** No events present on page{sections}')

    def test_003_for_mobile_tablet_expand_collapse_all_sections(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Expand/collapse all sections
        EXPECTED: * It is possible to expand/collapse every section
        EXPECTED: * Each expanded section contains valid names and time
        """
        if not self.device_type == 'desktop':
            sections = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg=f'*** No events present on page{sections}')

            for section_name, section in list(sections.items()):
                is_section_expanded = section.is_expanded()
                self.assertFalse(is_section_expanded,
                                 msg=f'The remaining section {section_name} is not collapsed after click')

                section.expand()
                sleep(2)
                is_section_expanded = section.is_expanded()
                self.assertTrue(is_section_expanded, msg=f'Cannot expand the section {section_name}')

            foot_events = sections['FOOTBALL'].items_as_ordered_dict
            self.assertTrue(foot_events, msg='*** No event present is "FOOTBALL" section')

            created_football_event = foot_events.get(self.event_name)
            self.assertTrue(created_football_event,
                            msg=f'Enhanced football event "{self.event_name2}" is not displayed')
            self.verify_event_start_time(created_football_event, self.event_name, self.eventID)
            self.assertEqual(created_football_event.name, self.event_name,
                             msg=f'Actual event name {created_football_event.name} does not '
                             f'match expected event name"{self.event_name}"')

            horse_events = sections['HORSE RACING'].items_as_ordered_dict
            self.assertTrue(foot_events, msg='*** No event present is "HORSE RACING" section')

            created_horse_event = horse_events.get(self.event_name2)
            self.assertTrue(created_horse_event, msg=f'Enhanced horse race event "{self.event_name2}" is not displayed')
            self.verify_event_start_time(created_horse_event, self.event_name2, self.eventID2)
            self.assertEqual(created_horse_event.name, self.event_name2,
                             msg=f'Actual event name {created_football_event.name} does not '
                             f'match expected event name"{self.event_name2}"')

    def test_004_verify_enhanced_multiples_outcomes_grouping(self):
        """
        DESCRIPTION: Verify Enhanced Multiples Outcomes grouping
        EXPECTED: Enhanced Multiples Outcomes are grouped by **CategoryID**
        """
        if not self.device_type == 'desktop':
            resp = self.ss_req.ss_event_for_type(type_id=self.type_id, query_builder=self.events_filter)
            events = [event['event'] for event in resp]
            for event in events:
                if self.event_name == event['name']:
                    self.assertEqual(event['categoryId'], self.ob_config.football_config.category_id,
                                     msg='Enhanced Multiples events are not grouped by **CategoryID**')

            resp2 = self.ss_req.ss_event_for_type(type_id=self.type_id2, query_builder=self.events_filter)
            events = [event['event'] for event in resp2]
            for event in events:
                if self.event_name == event['name']:
                    self.assertEqual(event['categoryId'], self.ob_config.horseracing_config.category_id,
                                     msg='Enhanced Multiples events are not grouped by **CategoryID**')
            sections = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            actual_list = list(sections.keys())

            expected_list = self.expected_name_section_list
            self.assertTrue(set(expected_list).issubset(actual_list),
                            msg=f'Incorrect sections sorting. Actual sections '
                            f'list "{actual_list}" does not match "{expected_list}')

    def test_005_verify_section_names(self):
        """
        DESCRIPTION: Verify section names
        EXPECTED: **For mobile/tablet:**
        EXPECTED: Sections are titled based on **CategoryName**
        EXPECTED: **For desktop:**
        EXPECTED: **CategoryName** is displayed on each 'Enhanced Multiples' card next to 'Enhanced' label
        """
        if self.device_type == 'desktop':
            self.__class__.sections = self.site.home.desktop_modules.enhanced_module.items_as_ordered_dict
            enhanced_module_list = []
            for section, item in self.sections.items():
                enhanced_module_name = item.header.text.replace('\n', ' ')
                enhanced_module_list.append(enhanced_module_name)

            self.assertIn('ENHANCED FOOTBALL', enhanced_module_list,
                          msg=f'Category name "FOOTBALL" displayed on "{enhanced_module_list}" card '
                          f'next to "Enhanced" label')
            self.assertIn('ENHANCED HORSE RACING', enhanced_module_list,
                          msg=f'Category name "HORSE RACING" displayed on "{enhanced_module_list}" card '
                          f'next to "Enhanced" label')
        else:
            sections = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            resp = self.ss_req.ss_event_for_type(type_id=self.type_id, query_builder=self.events_filter)
            events = [event['event'] for event in resp]
            section_name = sections['FOOTBALL'].sport_name
            for event in events:
                self.assertEqual(section_name, event['categoryName'].upper(),
                                 msg=f'Section"{section_name}" is not titled based on"{event["categoryName"].upper()}"')

            resp2 = self.ss_req.ss_event_for_type(type_id=self.type_id, query_builder=self.events_filter)
            events = [event['event'] for event in resp2]
            section_name = sections['HORSE RACING'].sport_name
            for event in events:
                self.assertEqual(section_name, event['categoryName'].upper(),
                                 msg=f'Section"{section_name}" is not titled based on"{event["categoryName"].upper()}"')

    def test_006_verify_sections_order(self):
        """
        DESCRIPTION: Verify sections order
        EXPECTED: **For mobile/tablet:**
        EXPECTED: Sections are ordered by the **Category displayOrder** in ascending
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel ordered by the **Category displayOrder** in ascending
        """
        if self.device_type == 'desktop':
            actual_list = []
            for section, item in self.sections.items():
                section_name = item.name.text
                actual_list.append(section_name)

            expected_list = self.expected_name_section_list
            self.assertTrue(set(expected_list).issubset(set(actual_list)),
                            msg=f'Incorrect sections sorting. Actual sections '
                            f'list "{actual_list}" does not match "{expected_list}')
        else:
            resp = self.ss_req.ss_event_for_type(type_id=self.type_id, query_builder=self.events_filter)
            events = [event['event'] for event in resp]
            for event in events:
                if self.event_name == event['name']:
                    self.assertEqual(event['displayOrder'], self.ob_config.football_config.category_id,
                                     msg='Enhanced Multiples events are not grouped by **Category displayOrder**')

            resp2 = self.ss_req.ss_event_for_type(type_id=self.type_id2, query_builder=self.events_filter)
            events = [event['event'] for event in resp2]
            for event in events:
                if self.event_name == event['name']:
                    self.assertEqual(event['displayOrder'], self.ob_config.horseracing_config.category_id,
                                     msg='Enhanced Multiples events are not grouped by **Category displayOrder**')

            sections = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            actual_list = list(sections.keys())
            expected_list = self.expected_name_section_list
            self.assertTrue(set(expected_list).issubset(actual_list),
                            msg=f'Incorrect sections sorting. Actual sections '
                            f'list "{actual_list}" does not match "{expected_list}')
