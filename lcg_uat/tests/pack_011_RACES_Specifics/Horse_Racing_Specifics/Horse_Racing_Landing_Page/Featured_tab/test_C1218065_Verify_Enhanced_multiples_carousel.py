import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.enhanced_multiples
@pytest.mark.mobile_only
@pytest.mark.races
@vtest
class Test_C1218065_Verify_Enhanced_multiples_carousel(BaseRacing):
    """
    TR_ID: C1218065
    VOL_ID: C9697753
    NAME: Verify Enhanced multiples carousel
    DESCRIPTION: This test case verifies that event type 'Enhanced Multiples' will be displayed as carousel on Featured tab in the 'Oxygen' application
    PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/*X.XX */EventToOutcomeForClass/227?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: 'typeName'='Enhanced Multiples'
    PRECONDITIONS: 'classID' on event level to see class id for selected event type
    PRECONDITIONS: 'className' on event level to see class name where event belongs to
    PRECONDITIONS: 'name' on event level to see event name and local time
    PRECONDITIONS: rawIsOffCode="Y" , **isStarted="true",** **rawIsOffCode="-" - **on event level to see whether event is started
    PRECONDITIONS: In case of several selections for one Enhanced Multiples market the same odd's price should be configured.
    """
    keep_browser_open = True
    enhanced_multiples_name = vec.racing.ENHANCED_MULTIPLES_NAME
    event_name1, event_name2, event_name3, event_name4 = None, None, None, None
    expected_events_order = []

    @staticmethod
    def get_enhanced_multiples_events_list_from_response(resp: list) -> list:
        """
        Having Siteserve response gets list of enhanced multiples events sorted in alphabetical order, ascending
        :param resp: Siteserve response (list of dicts)
        :return: list of enhanced multiples events in alphabetical order, ascending
        """
        events_list_ss = []
        for event_resp in resp:
            for market in event_resp['event']['children']:
                if market['market'].get('children'):
                    for outcome in market['market']['children']:
                        events_list_ss.append(f'{normalize_name(event_resp["event"]["name"])} - {outcome["outcome"]["name"]}')
        return sorted(events_list_ss)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing enhanced multiples event
        """
        event_params1 = self.ob_config.add_enhanced_multiples_racing_event(time_to_start=2)
        event_params2 = self.ob_config.add_enhanced_multiples_racing_event(time_to_start=20,
                                                                           number_of_runners=3,
                                                                           lp_prices={0: '1/5', 1: '9/1', 2: '1/5'})

        self.__class__.selection_ids1, self.__class__.selection_ids2 = \
            event_params1.selection_ids, event_params2.selection_ids

        self.__class__.event_name1 = f'{self.horseracing_autotest_enhanced_multiples_name_pattern} - {list(self.selection_ids1.keys())[0]}'

        expected_events_order_ = [x for _, x in sorted(zip(event_params2.selection_ids.values(),
                                                           event_params2.selection_ids.keys()))]

        expected_events_order_ = [f'{self.horseracing_autotest_enhanced_multiples_name_pattern} - {x}'
                                  for x in expected_events_order_]

        self.__class__.event_name2, self.__class__.event_name3, self.__class__.event_name4 = expected_events_order_

        self.__class__.expected_events_order = [self.event_name1]  # because it has lower start time
        self.__class__.expected_events_order.extend(expected_events_order_)
        self._logger.debug(f'*** Expected events order "{self.expected_events_order}"')

    def test_001_navigate_to_the_horse_racing_home_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' Home page
        EXPECTED: Horse Racing landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    def test_002_verify_enhanced_multiples_module(self):
        """
        DESCRIPTION: Verify 'Enhanced Multiples' module
        EXPECTED: 1. 'Enhanced Multiples' module is displayed as carousel
        EXPECTED: 2. 'Enhanced Multiples' module is expanded by default and "-" symbol should be displayed
        EXPECTED: 3. 'Enhanced Multiples' module is collapsed/expanded once tapped
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.enhanced_multiples_name, sections.keys(),
                      msg=f'Section "{self.enhanced_multiples_name}" not found in "{sections.keys()}"')

        self.__class__.enhanced_multiples_section = sections[self.enhanced_multiples_name]
        self.enhanced_multiples_section.scroll_to()

        is_expanded = self.enhanced_multiples_section.is_expanded()
        self.assertTrue(is_expanded, msg=f'Section "{self.enhanced_multiples_name}" is not expanded by default')

        self.__class__.events = self.enhanced_multiples_section.items_as_ordered_dict
        self.assertTrue(self.events, msg=f'No events found in section "{self.enhanced_multiples_name}"')
        self._logger.debug(f'*** Found events "{self.events.keys()}"')

        for event_name, event in self.events.items():
            event.scroll_to()
            self._logger.debug(f'*** Event "{event_name}" output price is "{event.bet_button.outcome_price_text}')
            self.assertTrue(event.bet_button.outcome_price_text,
                            msg=f'"Output price" is not displayed for event "{event_name}"')

    def test_003_verify_content_of_the_card(self):
        """
        DESCRIPTION: Verify content of the card
        EXPECTED: 1. Header title (is taken from event "name" attribute from SS response);
        EXPECTED: 2. Selection name (is taken from outcome "name" attribute from SS response);
        EXPECTED: 4. Clickable Odds button (adds selection to the Betslip)
        """
        self.assertIn(self.event_name1, self.events, msg=f'Event "{self.event_name1}" not found in "{self.events}"')
        self.assertIn(self.event_name2, self.events, msg=f'Event "{self.event_name2}" not found in "{self.events}"')
        self.assertIn(self.event_name3, self.events, msg=f'Event "{self.event_name3}" not found in "{self.events}"')
        self.assertIn(self.event_name4, self.events, msg=f'Event "{self.event_name4}" not found in "{self.events}"')

        self.events[self.event_name3].bet_button.click()
        self.site.wait_for_quick_bet_panel()
        self.site.quick_bet_panel.close()
        self.site.wait_quick_bet_overlay_to_hide()

    def test_004_verify_selections_ordering(self):
        """
        DESCRIPTION: Verify selections ordering
        EXPECTED: Selections are ordered by event 'startTime' attribute in asc order
        """
        set_2 = frozenset(self.expected_events_order)  # need to use frozen set to keep order of events
        intersection = [x for x in self.events.keys() if x in set_2]  # that's because there might be a lot more events than we create
        self.assertListEqual(intersection, self.expected_events_order)

    def test_005_verify_event_attributes_starttime_and_eventstatuscode(self):
        """
        DESCRIPTION: Verify event attributes 'startTime', 'eventStatusCode', 'isStarted' and 'outcomeStatusCode'
        EXPECTED: Only active and not started events are displayed in the section ('eventStatusCode='A', outcomeStatusCode='S' and 'isStarted'="true")
        """
        query_params = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A'))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, self.start_date_minus))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.EQUALS,
                                      self.ob_config.backend.ti.horse_racing.daily_racing_specials.enhanced_multiples.type_name))

        resp = self.ss_req.ss_event_to_outcome_for_class(
            class_id=self.ob_config.backend.ti.horse_racing.daily_racing_specials.class_id,
            query_builder=query_params)

        active_events = self.get_enhanced_multiples_events_list_from_response(resp=resp)
        ss_events = sorted([event.upper() for event in active_events])
        ui_events = sorted([event.upper() for event in self.events.keys()])
        self._logger.debug(f'*** List of active events from SiteServe: "{active_events}"')
        self.assertListEqual(ui_events, ss_events,
                             msg=f'Active events list "{ui_events}" '
                                 f'is not the same as got from SiteServe response "{ss_events}"')
