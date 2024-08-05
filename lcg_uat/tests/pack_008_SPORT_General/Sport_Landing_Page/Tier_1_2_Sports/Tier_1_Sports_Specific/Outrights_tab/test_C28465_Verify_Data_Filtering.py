import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28465_Verify_Data_Filtering(Common):
    """
    TR_ID: C28465
    NAME: Verify Data Filtering.
    DESCRIPTION: This test case verifies data filtering
    DESCRIPTION: **JIRA Tickets** :
    DESCRIPTION: * BMA-5106 'Market Filter for In-Play Events'
    DESCRIPTION: * BMA-9146 'Apply new design to Outrights and Enhanced Multiples'
    DESCRIPTION: * BMA-17707 'Remove Cash Out icons from the accordions on the Outrights tab'
    DESCRIPTION: **NOTE** :
    DESCRIPTION: for Football Sport only, Outright' tab is removed from the module header into 'Competition Module Header' within 'Matches' tab
    """
    keep_browser_open = True

    def get_event_and_market_from_ss(self, event_id: str) -> tuple:
        """
        Gets event and market for given event from SS response
        :param event_id: specifies event id
        :return: tuple with event and market attributes and their values
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        events = resp[0]['event']
        markets = resp[0]['event']['children'] if 'event' in resp[0] and 'children' in resp[0]['event'] else []
        return events, markets[0]['market']

    def verfiy_attributes(self, event_id, live_event=False):
        outright_event, outright_market = self.get_event_and_market_from_ss(event_id=event_id)
        eventSortCode = outright_event['eventSortCode']
        expected_eventSortCodes = vec.siteserve.OUTRIGHT_EVENT_SORT_CODES
        self.assertIn(eventSortCode, expected_eventSortCodes,
                      msg=f'Actual event sort code "{eventSortCode}" is not in Expected sort codes "{expected_eventSortCodes}"')
        if tests.settings.backend_env == 'prod' and 'isStarted' in outright_event.keys():
            live_event = True
        if live_event:
            isMarketBetInRun = outright_market['isMarketBetInRun']
            self.assertEqual(isMarketBetInRun, 'true', msg='Value of "isMarketBetInRun" is not "true"')
            rawIsOffCode = outright_event['rawIsOffCode'] in ['-', 'Y']
            self.assertTrue(rawIsOffCode, msg='Value of "rawIsOffCode" is not as expected')

    def test_000_preconditions(self):
        """
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
        if tests.settings.backend_env != 'prod':
            pre_match_event = self.ob_config.add_autotest_premier_league_football_outright_event()
            live_event = self.ob_config.add_autotest_premier_league_football_outright_event(is_live=True)
            self.__class__.pre_match_event_id, self.__class__.live_event_id = pre_match_event.event_id, live_event.event_id
            self.__class__.pre_match_event = pre_match_event.ss_response['event']['name']
            self.__class__.live_event = live_event.ss_response['event']['name']
            self.__class__.pre_match_event_section_name = pre_match_event.ss_response['event']['className'].replace("Football ", "") + " - " + \
                pre_match_event.ss_response['event']['typeName']

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        self.site.open_sport(name='FOOTBALL')
        current_tab_name = self.site.football.tabs_menu.current
        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is not "{expected_tab_name}", it is "{current_tab_name}"')
        if self.device_type == 'desktop':
            actual_date_tab_name = self.site.football.date_tab.current_date_tab
            self.assertEqual(actual_date_tab_name, vec.sb.SPORT_DAY_TABS.today,
                             msg=f'Actual date tab is "{actual_date_tab_name}" not "{vec.sb.SPORT_DAY_TABS.today}"')

    def test_003_go_to_outrights_events_page(self):
        """
        DESCRIPTION: Go to 'Outrights' Events page
        EXPECTED: *   'Outrights' Events page is opened
        EXPECTED: *   Navigation is carried out smoothly
        """
        outright_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper()
        outright_tab = self.site.football.tabs_menu.click_button(outright_tab_name)
        self.assertTrue(outright_tab, msg=f'"{outright_tab_name}" is not opened')

    def test_004_verify_list_of_events_in_each_section(self):
        """
        DESCRIPTION: Verify list of events in each section
        EXPECTED: **Pre-match events:**
        EXPECTED: Events with next attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20)
        EXPECTED: *   AND/OR **dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: **Started events:**
        EXPECTED: Events with the following attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20) AND/OR ​**dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        """
        if tests.settings.backend_env == 'prod':
            sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='markets are not listed')
            for section_name, section in list(sections.items())[0:3] if len(sections) > 3 else sections.items():
                section.expand()
                self.assertTrue(section.is_expanded(), msg=f'market "{section_name}" is not expanded')
                events = section.items_as_ordered_dict
                for event_name, event in list(events.items()):
                    event_id = event.template.event_id
                    self.verfiy_attributes(event_id=event_id)
        else:
            if self.brand == 'ladbrokes' and self.device_type == 'desktop':
                section_name = self.pre_match_event_section_name
            else:
                section_name = self.pre_match_event_section_name.upper()
            section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
            self.assertTrue(section, msg='markets are not listed')
            section.expand()
            self.assertTrue(section.is_expanded(), msg=f'market "{self.pre_match_event_section_name.upper()}" is not expanded')
            pre_event_created = section.items_as_ordered_dict.get(self.pre_match_event)
            self.assertTrue(pre_event_created,
                            msg=f'Created prematch event: "{self.pre_match_event}", id: "{self.pre_match_event_id}"  is not present')
            self.verfiy_attributes(event_id=self.pre_match_event_id)

            live_event_created = section.items_as_ordered_dict.get(self.live_event)
            self.assertTrue(live_event_created,
                            msg=f'Created live event: "{self.live_event}", id: "{self.live_event_id}"  is not present')
            self.verfiy_attributes(event_id=self.live_event_id, live_event=True)

    def test_005_verify_cash_out_label(self):
        """
        DESCRIPTION: Verify 'Cash out' label
        EXPECTED: 'CASH OUT' label is **NOT shown** next to event Type name in any case for Outright tab
        """
        # Cannot verify the unavailable elements
